import os
from enum import Enum

class AppConfig(Enum):
    SMTP_SERVER: str = os.environ["SMTP_SERVER"]
    SMTP_PORT: int = os.environ["SMTP_PORT"]
    SMTP_USERNAME: str = os.environ["SMTP_USERNAME"]
    SMTP_PASSWORD: str = os.environ["SMTP_PASSWORD"]
    STORAGE_PATH: str = os.environ["STORAGE_PATH"]