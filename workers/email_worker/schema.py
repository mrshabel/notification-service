from pydantic import BaseModel, EmailStr, HttpUrl
from enum import Enum

class NotificationEventType(str, Enum):
    USER_REGISTERED = "user_registered"
    PASSWORD_RESET = "password_reset"
    WELCOME = "welcome"
    VERIFICATION = "verification"
    
class BaseEmailSchema(BaseModel):
    email: EmailStr
    type: NotificationEventType

class WelcomeEmailSchema(BaseEmailSchema):
    pass

class VerificationEmailSchema(BaseEmailSchema):
    url: HttpUrl

class PasswordResetSchema(BaseEmailSchema):
    url: HttpUrl

class NotificationEmailSchema(BaseEmailSchema):
    content: str