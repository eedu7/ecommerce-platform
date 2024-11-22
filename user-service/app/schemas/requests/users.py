from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., min_length=8, max_length=64)
    username: str = Field(..., min_length=3, max_length=64, examples=["John.Doe"])


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., min_length=8, max_length=64)


class UserUpdateRequest(BaseModel):
    username: str = Field(..., examples=["john.doe"])
    profile_image_url: str = Field(
        ...,
    )
    phone_number: PhoneNumber = Field(
        ...,
    )


class UserPartialUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, examples=["john.doe"])
    profile_image_url: Optional[str] = Field(None)
    phone_number: Optional[PhoneNumber] = Field(
        None,
    )
