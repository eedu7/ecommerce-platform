from typing import Optional

from pydantic import BaseModel, Field


class ProfileUpdateRequest(BaseModel):
    username: str = Field(..., examples=["john.doe"])
    profile_image_url: str = Field(
        ...,
    )
    phone_number: str = Field(..., examples=["+92-3XX-XXXXXX"])


class ProfilePartialUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, examples=["john.doe"])
    profile_image_url: Optional[str] = Field(None)
    phone_number: str = Field(..., examples=["+92-3XX-XXXXXXX"])
