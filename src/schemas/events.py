from enum import Enum


class BrokerQueues(Enum):
    MAIN = "notification_events"
    EMAIL = "email_queue"


class Exchanges(Enum):
    AUTH = "auth_events"


class ExchangeTypes(Enum):
    AUTH = "topic"


class Queues(Enum):
    NOTIFICATION = "notification_queue"


class AuthEvents(Enum):
    # auth.user for user-related changes
    USER_REGISTERED = "auth.user.registered"
    PASSWORD_RESET_REQUESTED = "auth.user.password_reset"
    PASSWORD_RESET_COMPLETED = "auth.user.password_completed"
    ACCOUNT_VERIFIED = "auth.user.verified"
