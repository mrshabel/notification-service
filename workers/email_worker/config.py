import os
from enum import Enum
class Config():
    """
    The configuration to be used throughout the application
    """
    BROKER_HOST: str = os.environ["BROKER_HOST"]
    BROKER_PORT: int = os.environ["BROKER_PORT"]
    SMTP_SERVER: str = os.environ["SMTP_SERVER"]
    SMTP_PORT: int = os.environ["SMTP_PORT"]
    SMTP_USERNAME: str = os.environ["SMTP_USERNAME"]
    SMTP_PASSWORD: str = os.environ["SMTP_PASSWORD"]
    STORAGE_PATH: str = os.environ["STORAGE_PATH"]
    EMAIL_QUEUE: str = "email_queue"
    NOTIFICATION_EXCHANGE: str = "notifications"
    EMAIL_ROUTING_KEY: str = "email"
    APP_NAME: str = "Tetelestai"


AppConfig = Config()