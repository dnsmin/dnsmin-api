from pydantic import BaseModel, ConfigDict

from dnsmin.lib.services.powerdns.enums import AZoneRRSetChangeTypeEnum
from dnsmin.lib.services.powerdns.models import AZone as SAZone, AZoneRecord as SAZoneRecord, AZoneRRSet
from dnsmin.models.db.zones import AZone, AZoneRecord


class RecordChangeSet(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    new_records: list[AZoneRecord] = []
    update_records: list[AZoneRecord] = []
    delete_records: list[AZoneRecord] = []


def create_rrsets_from_db_azone(db_zone: AZone) -> list[AZoneRRSet]:
    record_map: dict[str, AZoneRRSet] = {}

    for record in db_zone.records:
        map_key = f'{record.type}-{record.name}'

        if map_key not in record_map:
            record_fqdn = record.name

            if record_fqdn == '@':
                record_fqdn = f'{db_zone.fqdn}.'
            else:
                record_fqdn += f'.{db_zone.fqdn}.'

            record_map[map_key] = AZoneRRSet(
                name=record_fqdn,
                type=record.type,
                ttl=record.ttl,
                changetype=AZoneRRSetChangeTypeEnum.REPLACE,
                records=[],
            )

        record_map[map_key].records.append(SAZoneRecord(content=record.content))

    return list(record_map.values())


def create_record_changeset_from_server_azone(db_zone: AZone, server_zone: SAZone) -> RecordChangeSet:
    cs = RecordChangeSet()

    return cs
