from enum import Enum
from pydantic import BaseModel


class NotificationChannel(Enum):
    EMAIL = "email"
    IN_APP = "in-app"
