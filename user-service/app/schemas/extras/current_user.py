from typing import Optional

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: Optional[int] = Field(None, description="User ID")

    class Config:
        validate_assignment = True
