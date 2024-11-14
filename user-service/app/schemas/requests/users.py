import re

from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=64)
    username: str = Field(..., min_length=3, max_length=64)


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=64)
