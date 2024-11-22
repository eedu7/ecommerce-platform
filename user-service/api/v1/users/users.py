from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.controllers import UserController
from app.models import User
from app.schemas.requests.users import (UserPartialUpdateRequest,
                                        UserUpdateRequest)
from app.schemas.responses.users import UserResponse, UserResponseDetail
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

user_router: APIRouter = APIRouter(
    dependencies=[Depends(AuthenticationRequired)],
)


@user_router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 20,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.get_all(skip, limit)


@user_router.get("/{user_uuid}", response_model=UserResponseDetail)
async def get_user_by_uuid(
    user_uuid: UUID,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> User:
    return await user_controller.get_user_by_uuid(user_uuid)


@user_router.delete("/{user_uuid}")
async def delete_user(
    user_uuid, user_controller: UserController = Depends(Factory().get_user_controller)
) -> JSONResponse:
    return await user_controller.delete_user(user_uuid)


@user_router.get("/me", response_model=UserResponseDetail)
def get_user(
    user: User = Depends(get_current_user),
) -> User:
    return user


@user_router.put("/", response_model=UserResponseDetail)
async def update_user_data(
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> User:
    return await user_controller.update_user(current_user.id, user_data)


@user_router.patch("/", response_model=UserResponseDetail)
async def update_user_data(
    user_data: UserPartialUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> User:
    return await user_controller.update_user(
        current_user.id, user_data, partial_update=True
    )
