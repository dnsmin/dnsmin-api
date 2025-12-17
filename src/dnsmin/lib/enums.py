from enum import Enum


class TimeUnitsEnum(str, Enum):
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'


class DayOfWeekEnum(str, Enum):
    SUNDAY = 'sunday'
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'


class NotificationCategoryEnum(str, Enum):
    ALERT = 'alert'
    TASK_RECEIVED = 'task_received'
    TASK_REVOKED = 'task_revoked'
    TASK_REJECTED = 'task_rejected'
    TASK_PRE_RUN = 'task_pre_run'
    TASK_POST_RUN = 'task_post_run'
    TASK_SUCCESS = 'task_success'
    TASK_RETRY = 'task_retry'
    TASK_FAILED = 'task_failed'
    TASK_INTERNAL_ERROR = 'task_internal_error'
    TASK_UNKNOWN = 'task_unknown'


class NotificationServiceEnum(str, Enum):
    MAIL = 'mail'
    MSTEAMS = 'msteams'
    TWILIO = 'twilio'


class TaskEnum(str, Enum):
    APP_ALERT = 'app.alert'
    APP_MAIL = 'app.mail'
    APP_MAIL_SEND = 'app.mail.send'
    APP_TEST = 'app.test'
    APP_TEST_MAIL = 'app.test.mail'
    APP_TEST_EXCEPTION = 'app.test.exception'
    APP_TEST_EXCEPTION_RETRY = 'app.test.exception_retry'
    APP_TEST_DELAY = 'app.test.delay'
    ZONES_COMPARISON = 'zones.comparison'


class TwilioNotificationTypeEnum(str, Enum):
    VOICE = 'voice'
    MESSAGE = 'message'
