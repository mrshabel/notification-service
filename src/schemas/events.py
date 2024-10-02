from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import datetime


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
    PASSWORD_RESET_COMPLETED = "auth.user.password_changed"
    ACCOUNT_VERIFIED = "auth.user.verified"


class BaseEventSchema(BaseModel):
    event_type: str
    timestamp: datetime = Field(default=datetime.now())

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class UserRegisteredEventSchema(BaseEventSchema):
    user_id: str
    email: EmailStr
    url: str

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class PasswordResetRequestedEventSchema(BaseEventSchema):
    user_id: str
    email: EmailStr
    url: str

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class PasswordResetCompletedEventSchema(BaseEventSchema):
    user_id: str
    email: EmailStr

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AccountVerifiedEventSchema(BaseEventSchema):
    user_id: str
    email: EmailStr

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
