from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    APP_NAME: str = "Notification Service"
    APP_DESCRIPTION: str = (
        "A microservice for emails, in-app, and push notifications"
    )
    ENVIRONMENT: Environment
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    BROKER_HOST: str
    BROKER_PORT: int
    NOTIFICATION_EXCHANGE: str = "notification_events"
    NOTIFICATION_QUEUE: str = "notification_queue"
    NOTIFICATION_EXCHANGE_TYPE: str = (
        "topic"  # allows chaining of routing keys
    )
    AUTH_EXCHANGE: str = "auth_events"
    EMAIL_ROUTING_KEY: str = "email"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
