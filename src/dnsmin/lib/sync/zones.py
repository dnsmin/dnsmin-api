from . import RedisStreamSyncWorker


class ZoneSyncWorker(RedisStreamSyncWorker):
    LOCK_TTL_SECONDS = 300

    def load_resource(self, zone_id: str):
        return (
            self.db_session.query(Zone)
            .filter(Zone.id == zone_id)
            .options(joinedload(Zone.records))
            .one()
        )

    def sync_resource(self, zone_id: str, zone):
        push_zone_to_dns_servers(zone)

    def mark_clean(self, zone_id: str):
        self.db_session.query(Zone).filter(Zone.id == zone_id).update(
            {"sync_status": "clean"}
        )
        self.db_session.commit()
