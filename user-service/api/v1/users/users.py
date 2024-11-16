from typing import List

from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.models import User
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

user_router: APIRouter = APIRouter()


@user_router.get(
    "/",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=List[UserResponse],
)
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> List[User]:
    users = await user_controller.get_all()
    return users
