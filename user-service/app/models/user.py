from typing import List
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import TimestampMixin, UserAuditMixin


class User(Base, TimestampMixin, UserAuditMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    username: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_image_url: Mapped[bool] = mapped_column(Unicode(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(Unicode(30), nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, uuid={self.uuid}, username={self.username}, email={self.email})"

    def __str__(self):
        return self.__repr__()
