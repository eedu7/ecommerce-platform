from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class UserAuditMixin:
    """Mixins class to add auditing fields for created_by, updated_by, and deleted_by"""

    @declared_attr
    def created_by(cls) -> Mapped[Optional[int]]:
        return mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def updated_by(cls) -> Mapped[Optional[int]]:
        return mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def deleted_by(cls) -> Mapped[Optional[int]]:
        return mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
