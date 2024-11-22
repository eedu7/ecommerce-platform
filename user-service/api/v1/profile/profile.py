from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.models import User
from app.schemas.requests.profile import (ProfilePartialUpdateRequest,
                                          ProfileUpdateRequest)
from app.schemas.responses.users import UserResponse, UserResponseDetail
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

profile_router: APIRouter = APIRouter()


@profile_router.get("/", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponseDetail:
    return user


@profile_router.put("/")
async def update_profile(
    user_data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.update_user(current_user.id, user_data)


@profile_router.patch("/")
async def update_profile(
    user_data: ProfilePartialUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return await user_controller.update_user(
        current_user.id, user_data, partial_update=True
    )
