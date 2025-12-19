#!/usr/bin/env python3
"""
receiver.py
Asyncio-based DNS NOTIFY listener + AXFR puller and optional AXFR acceptor.

Usage: configure masters and allowed sources via env or config file.
"""

import asyncio
import logging
import signal
import struct
import os
from typing import List, Optional, Callable, Tuple

import dns.message
import dns.query
import dns.rdatatype
import dns.exception
from aiohttp import web

# ---------- Configuration (env-friendly) ----------
BIND_HOST = os.environ.get("DNSMIN_BIND_HOST", "0.0.0.0")
NOTIFY_PORT = int(os.environ.get("DNSMIN_NOTIFY_PORT", "5354"))  # UDP for NOTIFY (non-root)
AXFR_LISTEN_PORT = int(os.environ.get("DNSMIN_AXFR_PORT", "5353"))  # TCP to accept pushes (optional)
HEALTH_PORT = int(os.environ.get("DNSMIN_HEALTH_PORT", "8000"))
MASTER_SERVERS = os.environ.get("DNSMIN_MASTERS", "")  # comma-separated "ip:port" entries
AXFR_TIMEOUT = int(os.environ.get("DNSMIN_AXFR_TIMEOUT", "30"))  # seconds
SHUTDOWN_TIMEOUT = int(os.environ.get("DNSMIN_SHUTDOWN_TIMEOUT", "15"))
LOG_LEVEL = os.environ.get("DNSMIN_LOG_LEVEL", "INFO")

# ---------- Logging ----------
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("zone-server")

# ---------- Hook: user-provided handler ----------
# Replace or monkeypatch this function with your processing logic.
async def handle_zone_transfer(zone_name: str, records: List[dns.message.Message]) -> None:
    """
    Called when a complete AXFR has been received (either accepted from incoming TCP,
    or pulled from a master).
    - zone_name: zone FQDN without trailing dot
    - records: list of dns.rrset or parsed items (we pass dns.message.Message objects from each packet)
    """
    # Example: just log summary. Replace with DB updates, enqueue tasks, etc.
    total_rrs = sum(len(m.answer) for m in records)
    logger.info("handle_zone_transfer: zone=%s messages=%d total_rrs=%d",
                zone_name, len(records), total_rrs)


# ---------- Utility: parse DNS over TCP (length-prefixed) ----------
async def read_dns_tcp_message(reader: asyncio.StreamReader, timeout: Optional[float] = None) -> Optional[bytes]:
    """
    Read one DNS message over TCP (2-byte length prefix). Returns raw wire bytes (without length prefix).
    """
    # read 2-byte length
    try:
        length_prefix = await asyncio.wait_for(reader.readexactly(2), timeout=timeout)
    except (asyncio.IncompleteReadError, asyncio.TimeoutError):
        return None
    length = struct.unpack("!H", length_prefix)[0]
    if length == 0:
        return None
    try:
        data = await asyncio.wait_for(reader.readexactly(length), timeout=timeout)
    except (asyncio.IncompleteReadError, asyncio.TimeoutError):
        return None
    return data


# ---------- AXFR puller (client) ----------
async def fetch_axfr_from_master(master_addr: str, zone: str, port: int = 53, timeout: int = AXFR_TIMEOUT) -> Optional[List[dns.message.Message]]:
    """
    Initiate an AXFR to `master_addr:port` for `zone`. Returns list of dns.message.Message objects (one per wire packet)
    or None on failure.
    """
    logger.info("Initiating AXFR pull for zone=%s from %s:%d", zone, master_addr, port)
    try:
        reader, writer = await asyncio.open_connection(master_addr, port)
    except Exception as e:
        logger.error("AXFR connection failed to %s:%d: %s", master_addr, port, e)
        return None

    try:
        # Build a DNS query for AXFR
        q = dns.message.make_query(zone, dns.rdatatype.AXFR)
        wire = q.to_wire()
        # prepend two-byte length
        writer.write(struct.pack("!H", len(wire)) + wire)
        await writer.drain()

        messages = []
        soa_seen_first = False
        soa_seen_last = False
        while True:
            raw = await read_dns_tcp_message(reader, timeout=timeout)
            if raw is None:
                break
            try:
                msg = dns.message.from_wire(raw)
            except Exception as e:
                logger.warning("Failed to parse DNS message from master: %s", e)
                continue

            messages.append(msg)

            # detect AXFR termination by presence of SOA that equals first SOA (start and end)
            # find SOA in answers:
            for rrset in msg.answer:
                if rrset.rdtype == dns.rdatatype.SOA:
                    if not soa_seen_first:
                        soa_seen_first = True
                        first_soa = rrset.to_text()
                        logger.debug("AXFR first SOA: %s", first_soa)
                    else:
                        # second SOA: end of AXFR
                        last_soa = rrset.to_text()
                        if last_soa == first_soa:
                            soa_seen_last = True
                            logger.debug("AXFR end SOA matches first; AXFR complete")
                            break
            if soa_seen_last:
                break

        # cleanup
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

        if not messages:
            logger.warning("AXFR returned zero messages for zone %s", zone)
            return None

        return messages

    except Exception as e:
        logger.exception("Error during AXFR pull: %s", e)
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        return None


# ---------- Notify UDP listener (receives NOTIFY) ----------
class NotifyProtocol(asyncio.DatagramProtocol):
    def __init__(self, on_notify: Callable[[str, Tuple[str,int]], None]):
        self.on_notify = on_notify
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        try:
            msg = dns.message.from_wire(data)
        except Exception as e:
            logger.debug("Failed to parse NOTIFY from %s: %s", addr, e)
            return

        # Build and send RFC 1996-compliant response
        try:
            response = dns.message.make_response(msg)
            response.set_rcode(dns.rcode.NOERROR)
            wire = response.to_wire()
            self.transport.sendto(wire, addr)
            logger.debug("Sent NOTIFY ACK to %s", addr)
        except Exception as e:
            logger.warning("Failed to send NOTIFY response to %s: %s", addr, e)
            return

        # Process NOTIFY questions
        for q in msg.question:
            zone = q.name.to_text().rstrip(".")
            logger.info("NOTIFY received and acknowledged for zone=%s from %s", zone, addr)

            # Schedule async handling (AXFR pull, debounce, etc.)
            asyncio.create_task(self.on_notify(zone, addr))


# ---------- AXFR acceptor: accept incoming TCP AXFR pushes (optional) ----------
async def handle_incoming_axfr(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info("peername")
    logger.info("Incoming TCP AXFR connection from %s", peer)
    messages = []
    try:
        while True:
            raw = await read_dns_tcp_message(reader, timeout=AXFR_TIMEOUT)
            if raw is None:
                break
            try:
                msg = dns.message.from_wire(raw)
                messages.append(msg)
            except Exception as e:
                logger.debug("Failed to parse incoming AXFR message: %s", e)
    except Exception as e:
        logger.exception("Error reading incoming AXFR: %s", e)
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    # Attempt to extract zone name from first query or first SOA
    zone_name = None
    if messages:
        # try question section in first message:
        first = messages[0]
        if first.question:
            zone_name = first.question[0].name.to_text().rstrip(".")
        else:
            # try first SOA rrset:
            for m in messages:
                for rr in m.answer:
                    if rr.rdtype == dns.rdatatype.SOA:
                        try:
                            zone_name = rr.name.to_text().rstrip(".")
                            break
                        except Exception:
                            pass
                if zone_name:
                    break

    if zone_name:
        logger.info("Incoming AXFR for zone %s complete with %d messages", zone_name, len(messages))
        await handle_zone_transfer(zone_name, messages)
    else:
        logger.warning("Incoming AXFR completed but zone name not detected; messages=%d", len(messages))


# ---------- Manager: coordinate tasks and graceful shutdown ----------
class ZoneServer:
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        self.shutdown_event = asyncio.Event()
        self.tasks = set()
        self.udp_transport = None
        self.tcp_server = None
        self.http_runner = None

    async def start(self):
        # Start UDP NOTIFY listener
        listen = (BIND_HOST, NOTIFY_PORT)
        logger.info("Starting NOTIFY UDP listener on %s:%d", *listen)
        transport, protocol = await self.loop.create_datagram_endpoint(
            lambda: NotifyProtocol(self._on_notify),
            local_addr=listen
        )
        self.udp_transport = transport

        # Start optional TCP AXFR acceptor (if you want master to push)
        logger.info("Starting AXFR TCP acceptor on %s:%d", BIND_HOST, AXFR_LISTEN_PORT)
        self.tcp_server = await asyncio.start_server(handle_incoming_axfr, BIND_HOST, AXFR_LISTEN_PORT)

        # Start simple HTTP health endpoint
        app = web.Application()
        app.add_routes([web.get("/health", self.health)])
        self.http_runner = web.AppRunner(app)
        await self.http_runner.setup()
        site = web.TCPSite(self.http_runner, BIND_HOST, HEALTH_PORT)
        await site.start()
        logger.info("Health endpoint listening on %s:%d", BIND_HOST, HEALTH_PORT)

    async def stop(self):
        logger.info("Shutting down DNSMin Receiver")
        if self.udp_transport:
            self.udp_transport.close()
        if self.tcp_server:
            self.tcp_server.close()
            await self.tcp_server.wait_closed()
        if self.http_runner:
            await self.http_runner.cleanup()

        # Cancel outstanding tasks (optionally wait for them)
        if self.tasks:
            logger.info("Waiting for %d in-flight tasks", len(self.tasks))
            await asyncio.wait(self.tasks, timeout=SHUTDOWN_TIMEOUT)

    async def health(self, request):
        return web.json_response({"status": "ok"})

    async def _on_notify(self, zone: str, addr):
        """
        Called by UDP NOTIFY handler. We will try to AXFR from configured masters.
        If MASTER_SERVERS is empty, we log and ignore (user must configure masters).
        """
        if not MASTER_SERVERS:
            logger.warning("Received NOTIFY for %s but no masters configured (ZONES_MASTERS empty)", zone)
            return

        # schedule the fetch task
        task = asyncio.create_task(self._fetch_and_handle(zone))
        self.tasks.add(task)
        def done_cb(t):
            self.tasks.discard(t)
        task.add_done_callback(done_cb)

    async def _fetch_and_handle(self, zone: str):
        masters = [m.strip() for m in MASTER_SERVERS.split(",") if m.strip()]
        last_exc = None
        for m in masters:
            parts = m.split(":")
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 53
            try:
                msgs = await fetch_axfr_from_master(host, zone, port=port)
                if msgs:
                    await handle_zone_transfer(zone, msgs)
                    return
            except Exception as e:
                last_exc = e
                logger.exception("AXFR attempt failed for master %s: %s", m, e)
        logger.error("AXFR for zone %s failed on all masters. last error=%s", zone, last_exc)

    async def run_until_shutdown(self):
        await self.start()
        # wait until shutdown_event is set
        await self.shutdown_event.wait()
        await self.stop()

    def trigger_shutdown(self):
        self.shutdown_event.set()


# ---------- Entrypoint ----------
async def main():
    server = ZoneServer()
    loop = asyncio.get_running_loop()

    # Signals for graceful shutdown
    for signame in ("SIGINT", "SIGTERM"):
        try:
            loop.add_signal_handler(getattr(signal, signame), lambda s=signame: server.trigger_shutdown())
        except NotImplementedError:
            # not supported on Windows
            pass

    logger.info("DNSMin Receiver starting")
    await server.run_until_shutdown()
    logger.info("DNSMin Receiver stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
