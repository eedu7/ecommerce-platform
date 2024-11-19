from pydantic import UUID4, BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    username: str = Field(..., examples=["john.doe"])
    uuid: UUID4 = Field(..., examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])

    class Config:
        form_attributes = True


class UserResponseDetail(UserResponse):
    phone_number: str | None = None
    is_admin: bool = Field(False, examples=["true", "false"])
    email_verified: bool
    profile_image_url: str | None = None
