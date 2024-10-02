from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import datetime
from src.schemas.notification import NotificationChannel


class UserSchema(BaseModel):
    id: str = Field(..., title="ID", description="The user's ID")
    email: EmailStr = Field(..., title="Email", description="The user's email")
    phone: int = Field(
        ...,
        title="Phone",
        description="The user's phone number",
        min_length=10,
        max_length=12,
    )
    created_at: datetime = Field(
        ...,
        title="Created At",
        description="Date and Time the user was created",
    )
    preferences: list[NotificationChannel]

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
