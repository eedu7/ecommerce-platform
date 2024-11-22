from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse

from app.models import User
from app.repositories import UserRepository
from app.schemas.requests.users import (UserPartialUpdateRequest,
                                        UserUpdateRequest)
from core.controller import BaseController
from core.exceptions import BadRequestException, NotFoundException


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def get_user_by_uuid(self, user_uuid: UUID) -> User:
        try:
            user: User = await self.get_by_uuid(user_uuid)
            if not user:
                raise NotFoundException(f"User with uuid '{user_uuid}' not found")
            return user
        except Exception as e:
            raise BadRequestException(f"Error getting user. {e}")

    async def get_by_username(self, username: str) -> User:
        return await self.user_repository.get_by_username(username)

    async def get_by_email(self, email: str) -> User:
        return await self.user_repository.get_by_email(email)

    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdateRequest | UserPartialUpdateRequest,
        partial_update: bool = False,
    ):
        user: User = await self.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User not found. {e}")
        if partial_update:
            user_data: Dict[str, Any] = user_data.model_dump(exclude_none=True)
        else:
            user_data: Dict[str, Any] = user_data.model_dump(exclude_none=True)

        try:
            return await self.update_model(user, user_data)
        except Exception as e:
            raise BadRequestException(f"Error updating user. {e}")

    async def delete_user(self, user_uuid: UUID):
        user: User = await self.get_user_by_uuid(user_uuid)
        try:
            await self.delete(user)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": f"User with UUID '{user_uuid}' deleted"},
            )
        except Exception as e:
            raise BadRequestException(f"Error deleting user. {e}")
