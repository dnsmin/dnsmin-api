import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dnsmin.lib.sync.models import SyncJobMetadata


class RedisStreamSyncWorker(ABC):
    """
    Reusable Redis Streams–based synchronization worker.

    Subclass this and override:
      - sync_resource(...)
    """

    # ---- Tunables (override in subclass if needed) ----
    STREAM_MAXLEN = 100_000
    LOCK_TTL_SECONDS = 300
    RECLAIM_INTERVAL_SECONDS = 60
    MIN_IDLE_RECLAIM_MS = 300_000
    READ_BLOCK_MS = 5000
    READ_COUNT = 1

    _redis: Redis

    _db: async_sessionmaker[AsyncSession]

    @property
    def redis(self) -> Redis:
        return self._redis

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        return self._db

    def __init__(
            self,
            *,
            redis: Redis,
            db: async_sessionmaker[AsyncSession],
            namespace: str,
            consumer_group: str,
            consumer_name: str,
            metadata_class: type[SyncJobMetadata] = SyncJobMetadata,
    ):
        self._redis = redis
        self._db = db
        self.namespace = namespace
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.metadata_class = metadata_class
        self._last_reclaim = 0

    # ------------------------------------------------------------------
    # Redis key helpers (namespaced)
    # ------------------------------------------------------------------

    def _stream_key(self) -> str:
        return f"{self.namespace}:sync:stream"

    def _dirty_key(self, resource_id: str) -> str:
        return f"{self.namespace}:sync:dirty:{resource_id}"

    def _lock_key(self, resource_id: str) -> str:
        return f"{self.namespace}:sync:lock:{resource_id}"

    def _inflight_key(self, resource_id: str) -> str:
        return f"{self.namespace}:sync:inflight:{resource_id}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def init(self):
        await self._ensure_consumer_group()

    async def mark_dirty(self, resource_id: str, metadata: Optional[SyncJobMetadata] = None):
        """
        Mark a resource as changed and enqueue it for sync.
        """
        ts = int(time.time())
        await self.redis.set(self._dirty_key(resource_id), ts)

        if not isinstance(metadata, SyncJobMetadata):
            metadata = self.metadata_class(resource_id=resource_id, ts=ts)
        else:
            metadata.resource_id = resource_id
            metadata.ts = ts

        await self.redis.xadd(
            self._stream_key(),
            metadata.model_dump(mode='json'),
            maxlen=self.STREAM_MAXLEN,
            approximate=True,
        )

    async def run_forever(self):
        """
        Main worker loop.
        """
        import asyncio
        from loguru import logger

        logger.info(f'Starting synchronization worker {self.consumer_name} for {self.namespace}:{self.consumer_group}.')

        while True:
            try:
                await self._iteration()
            except asyncio.CancelledError:
                break

    async def shutdown(self):
        from loguru import logger
        logger.info(f'Shutting down synchronization worker {self.consumer_name} for {self.namespace}:{self.consumer_group}.')

    # ------------------------------------------------------------------
    # Core message handling
    # ------------------------------------------------------------------

    async def _iteration(self):
        """Provides the iteration cycle workflow of the long-running worker."""

        await self._maybe_reclaim()

        entries = await self.redis.xreadgroup(
            groupname=self.consumer_group,
            consumername=self.consumer_name,
            streams={self._stream_key(): ">"},
            count=self.READ_COUNT,
            block=self.READ_BLOCK_MS,
        )

        if not entries:
            return

        _, messages = entries[0]
        for msg_id, data in messages:
            await self._handle_message(msg_id, self.metadata_class(**data))

    async def _handle_message(self, msg_id: str, metadata: SyncJobMetadata):
        token = await self._acquire_lock(metadata.resource_id)
        if not token:
            await self._ack(msg_id)
            return

        try:
            await self._process_resource(metadata.resource_id, metadata)
            await self._ack(msg_id)
        except Exception:
            # Leave pending for retry
            raise
        finally:
            await self._release_lock(metadata.resource_id, token)

    async def _process_resource(self, resource_id: str, metadata: SyncJobMetadata):
        dirty_key = self._dirty_key(resource_id)
        inflight_key = self._inflight_key(resource_id)

        dirty_before = self.redis.get(dirty_key)

        await self.redis.set(inflight_key, time.time(), ex=self.LOCK_TTL_SECONDS)

        # Perform actual sync (SUBCLASS MUST IMPLEMENT)
        await self.sync_resource(resource_id, metadata)

        dirty_after = await self.redis.get(dirty_key)

        if dirty_before == dirty_after:
            await self.redis.delete(dirty_key)
            await self.mark_clean(resource_id, metadata)
        else:
            # Changed during sync → requeue
            metadata.reason = "changed_during_sync"
            await self.mark_dirty(resource_id, metadata)

    # ------------------------------------------------------------------
    # Locking
    # ------------------------------------------------------------------

    async def _acquire_lock(self, resource_id: str) -> Optional[str]:
        token = str(uuid.uuid4())
        ok = await self.redis.set(
            self._lock_key(resource_id),
            token,
            nx=True,
            ex=self.LOCK_TTL_SECONDS,
        )
        return token if ok else None

    async def _release_lock(self, resource_id: str, token: str):
        lua = """
        if redis.call("GET", KEYS[1]) == ARGV[1] then
            return redis.call("DEL", KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(lua, 1, self._lock_key(resource_id), token)

    # ------------------------------------------------------------------
    # Reclaim logic
    # ------------------------------------------------------------------

    async def _maybe_reclaim(self):
        now = time.time()
        if now - self._last_reclaim < self.RECLAIM_INTERVAL_SECONDS:
            return

        self._last_reclaim = now

        pending = await self.redis.xpending_range(
            self._stream_key(),
            self.consumer_group,
            min="-",
            max="+",
            count=10,
        )

        for entry in pending:
            if entry["idle"] > self.MIN_IDLE_RECLAIM_MS:
                await self.redis.xclaim(
                    self._stream_key(),
                    self.consumer_group,
                    self.consumer_name,
                    min_idle_time=self.MIN_IDLE_RECLAIM_MS,
                    message_ids=[entry["message_id"]],
                )

    # ------------------------------------------------------------------
    # Redis helpers
    # ------------------------------------------------------------------

    async def _ack(self, msg_id: str):
        await self.redis.xack(self._stream_key(), self.consumer_group, msg_id)

    async def _ensure_consumer_group(self):
        try:
            await self.redis.xgroup_create(
                self._stream_key(),
                self.consumer_group,
                id="$",
                mkstream=True,
            )
        except Exception:
            pass  # group already exists

    # ------------------------------------------------------------------
    # Hooks for subclasses
    # ------------------------------------------------------------------

    async def mark_clean(self, resource_id: str, metadata: SyncJobMetadata):
        """
        Persist clean state to SQL if desired.
        Optional override.
        """
        pass

    @abstractmethod
    async def sync_resource(self, resource_id: str, metadata: SyncJobMetadata):
        """
        Perform the expensive external sync.
        MUST be idempotent.
        """
        raise NotImplementedError
