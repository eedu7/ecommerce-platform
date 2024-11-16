from fastapi import APIRouter, Depends

from app.models import User
from app.schemas.responses.users import UserResponse
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

profile_router: APIRouter = APIRouter()


@profile_router.get(
    "/", dependencies=[Depends(AuthenticationRequired)], response_model=UserResponse
)
def get_user(
    user: User = Depends(get_current_user),
) -> User:
    return user
