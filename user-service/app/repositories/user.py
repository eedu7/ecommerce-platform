from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(self, username: str) -> User | None:
        return await self.get_by(field="username", value=username)

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_by(field="email", value=email)
