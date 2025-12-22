"""
Task Database Models

This file defines the database models associated with task functionality.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, DECIMAL, Integer, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dnsmin.app import DB_PREFIX
from dnsmin.models.db import BaseSqlModel, JSONType
from dnsmin.models.enums import TaskJobStatusEnum


class TaskJob(BaseSqlModel):
    """Represents a task job."""

    __tablename__ = f'{DB_PREFIX}_task_jobs'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """The unique identifier of the task job."""

    root_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the Celery root task associated with this task."""

    parent_id: Mapped[Optional[UUID]] = mapped_column(Uuid, nullable=True)
    """The unique identifier of the Celery parent task associated with this task."""

    task_id: Mapped[Optional[UUID]] = mapped_column(Uuid, nullable=False)
    """The unique identifier of the Celery task associated with this task."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The name of the Celery task."""

    args: Mapped[Optional[list]] = mapped_column(JSONType, nullable=True)
    """The arguments of the Celery task."""

    kwargs: Mapped[Optional[dict]] = mapped_column(JSONType, nullable=True)
    """The keyword arguments of the Celery task."""

    options: Mapped[Optional[dict]] = mapped_column(JSONType, nullable=True)
    """The options of the Celery task."""

    retries: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    """The total number of execution retries performed."""

    runtime: Mapped[Optional[float]] = mapped_column(DECIMAL(14, 6), nullable=True)
    """The total runtime of the task job in seconds."""

    output: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The captured STDOUT and STDERR of the task job."""

    errors: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The captured exception stacktraces of the task job."""

    status: Mapped[TaskJobStatusEnum] = mapped_column(String(20), nullable=False)
    """The current status of the task job."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the task job was created."""

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the task job was last updated."""

    started_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    """The timestamp representing when the task job was started."""

    ended_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    """The timestamp representing when the task job was completed."""

    activities = relationship('TaskJobActivity', back_populates='task_job', cascade='all, delete, delete-orphan')
    """A list of activities associated with the task job."""


class TaskJobActivity(BaseSqlModel):
    """Represents a task job activity update."""

    __tablename__ = f'{DB_PREFIX}_task_job_activities'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the activity."""

    task_job_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_task_jobs.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the task job associated with this activity update."""

    error: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The captured exception stacktrace of a failed task job execution."""

    status: Mapped[TaskJobStatusEnum] = mapped_column(String(20), nullable=False)
    """The status of the task job for the activity update."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the activity was created."""

    task_job = relationship('TaskJob', back_populates='activities', cascade='expunge')
    """The task job associated with the activity update."""
