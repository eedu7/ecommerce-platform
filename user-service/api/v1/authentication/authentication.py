from fastapi import APIRouter, Depends, status

from app.controllers import AuthController
from app.models import User
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory

auth_router: APIRouter = APIRouter()


@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> User:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )


@auth_router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )
