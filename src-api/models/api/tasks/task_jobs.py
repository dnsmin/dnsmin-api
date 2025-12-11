from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import TaskJobStatusEnum


class TaskJobOutSchema(BaseApiModel):
    """Provides an API response model for representing task jobs."""

    id: UUID = Field(
        title='Task Job ID',
        description='The unique identifier of the task job.',
        examples=[uuid4()],
    )
    """The unique identifier of the task job."""

    root_id: UUID = Field(
        title='Root ID',
        description='The unique identifier of the Celery root task associated with this task.',
        examples=[uuid4()],
    )
    """The unique identifier of the Celery root task associated with this task."""

    parent_id: Optional[UUID] = Field(
        title='Parent ID',
        description='The unique identifier of the Celery parent task associated with this task.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the Celery parent task associated with this task."""

    task_id: UUID = Field(
        title='Task ID',
        description='The unique identifier of the Celery task associated with this task.',
        examples=[uuid4()],
    )
    """The unique identifier of the Celery task associated with this task."""

    name: str = Field(
        title='Task Name',
        description='The name of the Celery task.',
    )
    """The name of the Celery task."""

    args: Optional[list] = Field(
        title='Task Arguments',
        description='The arguments of the Celery task.',
        default=None,
    )
    """The arguments of the Celery task."""

    kwargs: Optional[dict] = Field(
        title='Task Keyword Arguments',
        description='The keyword arguments of the Celery task.',
        default=None,
    )
    """The keyword arguments of the Celery task."""

    options: Optional[dict] = Field(
        title='Task Options',
        description='The options of the Celery task.',
        default=None,
    )
    """The options of the Celery task."""

    retries: int = Field(
        title='Task Retries',
        description='The total number of execution retries performed.',
    )
    """The total number of execution retries performed."""

    runtime: Optional[float] = Field(
        title='Task Runtime',
        description='The total runtime of the task job in seconds.',
        default=None,
    )
    """The total runtime of the task job in seconds."""

    output: Optional[str] = Field(
        title='Task Output',
        description='The captured STDOUT and STDERR of the task job.',
        default=None,
    )
    """The captured STDOUT and STDERR of the task job."""

    errors: Optional[str] = Field(
        title='Task Errors',
        description='The captured exception stacktraces of the task job.',
        default=None,
    )
    """The captured exception stacktraces of the task job."""

    status: TaskJobStatusEnum = Field(
        title='Task Status',
        description='The current status of the task job.',
        examples=[TaskJobStatusEnum.received, TaskJobStatusEnum.running, TaskJobStatusEnum.success],
    )
    """The current status of the task job."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the task job was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the task job was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the task job was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the task job was last updated."""

    started_at: Optional[datetime] = Field(
        title='Started At',
        description='The timestamp representing when the task job was started.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the task job was started."""

    ended_at: Optional[datetime] = Field(
        title='Ended At',
        description='The timestamp representing when the task job was completed.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the task job was completed."""


class TaskJobActivityOutSchema(BaseApiModel):
    """Provides an API response model for representing task job activities."""

    id: UUID = Field(
        title='Task Job ID',
        description='The unique identifier of the task job.',
        examples=[uuid4()],
    )
    """The unique identifier of the task job."""

    task_job_id: UUID = Field(
        title='Task Job ID',
        description='The unique identifier of the task job associated with this activity update.',
        examples=[uuid4()],
    )
    """The unique identifier of the task job associated with this activity update."""

    error: Optional[str] = Field(
        title='Task Error',
        description='The captured exception stacktrace of a failed task job execution.',
        default=None,
    )
    """The captured exception stacktrace of a failed task job execution."""

    status: TaskJobStatusEnum = Field(
        title='Task Status',
        description='The status of the task job for the activity update.',
        examples=[TaskJobStatusEnum.received, TaskJobStatusEnum.running, TaskJobStatusEnum.success],
    )
    """The status of the task job for the activity update."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the task job was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the task job was created."""


class TaskJobsSchema(BaseApiModel):
    """Provides an API response model for retrieving task jobs."""

    records: list[TaskJobOutSchema] = Field(
        title='Task Jobs',
        description='A list of task jobs found based on the current request criteria.',
        default_factory=list,
    )
    """A list of task jobs found based on the current request criteria."""

    total: int = Field(
        title='Total Task Jobs',
        description='The total number of task jobs.',
        default=0,
        examples=[1234],
    )
    """The total number of task jobs."""

    total_filtered: int = Field(
        title='Total Task Jobs Found',
        description='The total number of task jobs found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of task jobs found based on the current request criteria."""


class TaskJobActivitiesSchema(BaseApiModel):
    """Provides an API response model for retrieving task job activities."""

    records: list[TaskJobActivityOutSchema] = Field(
        title='Task Job Activities',
        description='A list of task job activities found based on the current request criteria.',
        default_factory=list,
    )
    """A list of task job activities found based on the current request criteria."""

    total: int = Field(
        title='Total Task Job Activities',
        description='The total number of task job activities.',
        default=0,
        examples=[1234],
    )
    """The total number of task job activities."""

    total_filtered: int = Field(
        title='Total Task Job Activities Found',
        description='The total number of task job activities found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of task job activities found based on the current request criteria."""
