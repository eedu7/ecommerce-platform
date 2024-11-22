from pydantic import UUID4, BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    uuid: UUID4 = Field(..., examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])
    username: str = Field(..., examples=["john.doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])


class UserResponseDetail(UserResponse):
    profile_image_url: str | None = None
    phone_number: str | None = None
    is_admin: bool = Field(False, examples=["true", "false"])
    email_verified: bool

    class Config:
        form_attributes = True
