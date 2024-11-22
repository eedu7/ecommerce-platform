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
    address_type: AddressType = Field(
        AddressType.SHIPPING, examples=[AddressType.SHIPPING, AddressType.BILLING]
    )


class AddressUpdateRequest(BaseModel):
    street_address: str = Field(..., examples=["123-A Main Street"])
    apartment: str = Field(..., examples=["Apt 128"])
    city: str = Field(..., examples=["Karachi"])
    state: str = Field(..., examples=["Sindh"])
    country: str = Field(..., examples=["Pakistan"])
    postal_code: str = Field(..., examples=["7400"])
    address_type: AddressType = Field(
        AddressType.SHIPPING, examples=[AddressType.SHIPPING, AddressType.BILLING]
    )


class AddressPartialUpdateRequest(BaseModel):
    street_address: Optional[str] = Field(None, examples=["123-A Main Street"])
    apartment: Optional[str] = Field(None, examples=["Apt 128"])
    city: Optional[str] = Field(None, examples=["Karachi"])
    state: Optional[str] = Field(None, examples=["Sindh"])
    country: Optional[str] = Field(None, examples=["Pakistan"])
    postal_code: Optional[str] = Field(None, examples=["7400"])
    address_type: Optional[AddressType] = Field(
        None, examples=[AddressType.SHIPPING, AddressType.BILLING]
    )
