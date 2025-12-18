#!/usr/bin/env python3
import asyncio
import signal
import uuid

from signal import Signals
from typing import Literal

from dnsmin.lib import load_environment, load_settings, init_redis, init_sql
from dnsmin.lib.config import AppConfig
from dnsmin.lib.sync import RedisStreamSyncWorker
from dnsmin.lib.sync.zones import ZoneSyncWorker

WORKER_COUNT = 4
NAMESPACE = "dns"
CONSUMER_GROUP = "dns-sync"


async def run_worker(worker: RedisStreamSyncWorker):
    try:
        await worker.run_forever()
    finally:
        await worker.shutdown()


async def main():
    env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default

    load_environment(env_prefix)

    settings = load_settings(env_prefix)

    if settings.env_prefix != env_prefix:
        settings = load_settings(env_prefix=settings.env_prefix)

    redis = init_redis(settings.config)
    db_engine, db_session = init_sql(settings.config, use_sync=False)

    tasks = []

    for i in range(WORKER_COUNT):
        worker = ZoneSyncWorker(
            redis=redis,
            db_session=db_session,
            namespace=NAMESPACE,
            consumer_group=CONSUMER_GROUP,
            consumer_name=f"sync-worker-{i+1}-{uuid.uuid4().hex[:6]}",
        )

        await worker.init()

        task = asyncio.create_task(run_worker(worker))
        tasks.append(task)

    # Graceful shutdown
    stop_event = asyncio.Event()

    def _stop(stop_signal: Literal[Signals.SIGINT, Signals.SIGTERM]):
        from loguru import logger
        signal_label = f'{stop_signal}'

        if stop_signal is Signals.SIGINT:
            signal_label = 'SIGINT'
        elif stop_signal is Signals.SIGTERM:
            signal_label = 'SIGTERM'

        logger.info(f'Worker process received {signal_label} signal. Shutting down...')
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, _stop, signal.SIGTERM)
    loop.add_signal_handler(signal.SIGINT, _stop, signal.SIGINT)

    await stop_event.wait()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

    await redis.aclose()
    await db_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
