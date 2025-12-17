from typing import Callable
from prometheus_fastapi_instrumentator.metrics import Info
from dnsmin.app import DB_PREFIX

STATUS_MAP = {
    'received': 1,
    'running': 2,
    'retry': 3,
    'success': 4,
    'failed': -1,
    'revoked': -2,
}

STATUS_SQL = f"""
WITH ranked_jobs AS (
    SELECT
        name,
        status,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY name ORDER BY created_at DESC) AS rn
    FROM {DB_PREFIX}_task_jobs
)
SELECT name, status
FROM ranked_jobs
WHERE rn = 1;
"""

def metric_last_task_status() -> Callable[[Info], None]:
    from prometheus_client.metrics import Gauge
    from sqlalchemy import text

    metric = Gauge(
        'last_task_status',
        'The last execution status of a task.',
        labelnames=('task',),
    )

    def instrumentation(info: Info) -> None:
        from dnsmin.app import SessionLocal
        with SessionLocal() as session:
            result = session.execute(text(STATUS_SQL)).fetchall()

        for row in result:
            status_code = 0

            if row[1] in STATUS_MAP:
                status_code = STATUS_MAP[row[1]]

            metric.labels(task=row[0]).set(status_code)

    return instrumentation

def metric_setup(metrics):
    metrics.add(metric_last_task_status())
