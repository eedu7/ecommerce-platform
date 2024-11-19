from fastapi import APIRouter, Depends

from app.models import User
from app.schemas.responses.users import UserResponse, UserResponseDetail
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

profile_router: APIRouter = APIRouter()


@profile_router.get("/", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponseDetail:
    return user


@profile_router.put("/")
async def update_profile(user: User = Depends(get_current_user)):
    return {"message": "User updated", "user": user}


@profile_router.put("/password")
async def update_password(user: User = Depends(get_current_user)):
    return {"message": "User password updated", "user": user}
