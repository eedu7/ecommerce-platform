from typing import Sequence

from app.models import Address
from core.repository import BaseRepository


class AddressRepository(BaseRepository[Address]):
    """
    Address repository to get all database operations for the address model
    """

    async def get_by_user_address(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> Sequence[Address]:
        return await self.get_all(skip, limit, filters={"user_id": user_id})
