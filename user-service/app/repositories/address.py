from app.models import Address
from core.repository import BaseRepository


class AddressRepository(BaseRepository[Address]):
    """
    Address repository to get all database operations for the address model
    """

    async def get_by_user_id(
        self, user_id: str, join_: set[str] | None = None, unique: bool = False
    ):
        """
        Get user by username.

        :param user_id: User ID or UUID.
        :param join_: Join relations.
        :param unique: Unique relations.
        :return: User.
        """
        return await self.get_by(
            field="user_id", value=user_id, join_=join_, unique=unique
        )
