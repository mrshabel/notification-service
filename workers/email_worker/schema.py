from pydantic import BaseModel, EmailStr, HttpUrl

class BaseEmailSchema(BaseModel):
    email: EmailStr

class WelcomeEmailSchema(BaseEmailSchema):
    pass

class VerificationEmailSchema(BaseEmailSchema):
    url: HttpUrl

class PasswordResetSchema(BaseEmailSchema):
    url: HttpUrl

class NotificationEmailSchema(BaseEmailSchema):
    content: str