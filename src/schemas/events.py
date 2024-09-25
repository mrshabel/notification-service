from enum import Enum


class BrokerQueues(Enum):
    MAIN = "notification_events"
    EMAIL = "email_queue"
