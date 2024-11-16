from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from core.database.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "authentication"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    username: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"ID: {self.id}, username: {self.username}"

    def __str__(self):
        return self.__repr__()
