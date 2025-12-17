from celery import current_app

from dnsmin.lib.enums import TaskEnum


@current_app.task(name=TaskEnum.ZONES_COMPARISON.value, label='Zones Comparison')
def zones_comparison():
    """Compares DNSMin zones with those on registered servers and queues synchronization accordingly."""
    from loguru import logger
    from dnsmin.worker import app as celery_app

    logger.info(f'Starting zone comparison task.')

    logger.info(f'Completed zone comparison task.')
