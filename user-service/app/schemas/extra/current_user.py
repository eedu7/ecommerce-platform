from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: int = Field(..., description="User ID")

    class Config:
        validate_assignment = True
