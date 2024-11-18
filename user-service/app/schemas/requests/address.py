from typing import Optional

import pycountry
from pydantic import BaseModel, Field, field_validator

from app.models import AddressType


class AddressRequest(BaseModel):
    street_address: str = Field(..., examples=["123-A Main Street"])
    apartment: Optional[str] = Field(None, examples=["Apt 128"])
    city: str = Field(..., examples=["Karachi"])
    state: Optional[str] = Field(None, examples=["Sindh"])
    country: str = Field(..., examples=["Pakistan"])
    postal_code: Optional[str] = Field(None, examples=["7400"])
    address_type: AddressType = Field(AddressType.SHIPPING, examples=["SHIPPING"])

    @field_validator("city")
    def validate_country(cls, country: str) -> str:
        if not pycountry.countries.get(name=country):
            raise ValueError(f"Country {country} is not a valid country")
        return country

    @field_validator("state")
    def validate_state(cls, state, values):
        country = values.get("country")
        if country:
            subdivisions = pycountry.subdivisions.get(
                country_code=pycountry.countries.get(name=country).alpha_2
            )
            valid_states = (
                {subdivision.name for subdivision in subdivisions}
                if subdivisions
                else {}
            )
            if state not in valid_states:
                raise ValueError(
                    f"State '{state}' is not valid for the country '{country}'."
                )
        return state
