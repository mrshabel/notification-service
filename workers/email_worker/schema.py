from enum import Enum

class NotificationEventType(str, Enum):
    USER_REGISTERED = "user_registered"
    PASSWORD_RESET = "password_reset"
    WELCOME = "welcome"
    VERIFICATION = "verification"