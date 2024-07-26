from pydantic import Field, BaseModel, EmailStr, ConfigDict, UUID4
from pydantic.alias_generators import to_camel
from datetime import datetime


class EmailBaseSchema(BaseModel):
    sender: EmailStr = Field(
        ..., title="Sender Email", description="Email address of the sender"
    )
    recipient: EmailStr = Field(
        ...,
        title="Recipient Email",
        description="Email address of the recipient",
    )
    subject: str = Field(
        ..., title="Subject", description="Subject of the email"
    )
    body: str = Field(..., title="Body", description="Body of the email")
    is_read: bool = Field(
        default=False,
        title="Is Read",
        description="Indicate if the message is read or not",
    )

    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class CreateEmailSchema(EmailBaseSchema):
    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class EmailSchema(EmailBaseSchema):
    id: UUID4 = Field(..., title="Email ID", description="ID of the email")
    created_at: datetime = Field(
        title="Created At",
        description="Date and time the email was created",
        default=datetime.now(),
    )

    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class SuccessResponse(BaseModel):
    message: str = Field(
        title="Message", description="The success response", default="success"
    )
    data: EmailSchema = Field(title="Data", description="The email data")


class MultiDataSuccessResponse(BaseModel):
    message: str = Field(
        title="Message", description="The success response", default="success"
    )
    data: list[EmailSchema] = Field(
        title="Data", description="A list of email data", default=[]
    )
    count: int = Field(
        title="Count", description="The total number of emails", default=0
    )
