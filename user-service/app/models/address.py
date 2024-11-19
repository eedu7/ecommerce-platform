from enum import StrEnum
from typing import Optional
from uuid import uuid4

from sqlalchemy import BigInteger, Enum, ForeignKey, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import TimestampMixin, UserAuditMixin


class AddressType(StrEnum):
    SHIPPING: str = "shipping"
    BILLING: str = "billing"


class Address(Base, TimestampMixin, UserAuditMixin):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, unique=True, nullable=False
    )
    street_address: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    apartment: Mapped[Optional[str]] = mapped_column(Unicode(255), nullable=True)
    city: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    state: Mapped[Optional[str]] = mapped_column(Unicode(100), nullable=True)
    country: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    postal_code: Mapped[Optional[str]] = mapped_column(Unicode(20), nullable=True)
    address_type: Mapped[AddressType] = mapped_column(
        Enum(AddressType), default=AddressType.SHIPPING
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )

    def __repr__(self):
        """Returns a detailed string representation of the Address instance."""
        return (
            f"Address(id={self.id}, uuid={self.uuid}, street_address='{self.street_address}', "
            f"apartment='{self.apartment}', city='{self.city}', state='{self.state}', "
            f"country='{self.country}', postal_code='{self.postal_code}', "
            f"address_type='{self.address_type}', user_id={self.user_id})"
        )

    def __str__(self):
        """Returns a user-friendly string representation of the Address instance."""
        return (
            f"{self.street_address}, {self.apartment if self.apartment else ''}, {self.city}, "
            f"{self.state if self.state else ''}, {self.country}, {self.postal_code}"
        )
