from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    APP_NAME: str = "Notification Service"
    APP_DESCRIPTION: str = "A microservice for emails, in-app, and push notifications"
    ENVIRONMENT: Environment
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()