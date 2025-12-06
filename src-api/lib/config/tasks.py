from typing import Union
from lib.config.base import BaseConfig


class TaskSchedule(BaseConfig):
    enabled: bool = True
    key: Union[str, None] = None
    name: str
    task: str
    at: Union[list[str], str, None] = None
    args: Union[list, None] = None
    kwargs: Union[dict, None] = None
    options: Union[dict, None] = None


class TasksConfig(BaseConfig):
    class TaskSchedulerConfig(BaseConfig):
        tick_interval: int = 30
        max_schedule_lifetime: int = 30

    enabled: bool = True
    scheduler: TaskSchedulerConfig
