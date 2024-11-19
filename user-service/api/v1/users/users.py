from fastapi import APIRouter, Depends

from app.models import User
from core.fastapi.dependencies import get_current_user

user_router: APIRouter = APIRouter()


@user_router.get("/")
async def get_users():
    return {
        "message": "Getting user details",
        "task": "For admin to get all user details",
    }


@user_router.post("/{user_id}")
async def get_user_detail(user_id: str):
    return {
        "message": "Getting user details",
        "task": "For admin to get user details by user id",
    }


@user_router.delete("/")
async def delete_user(user: User = Depends(get_current_user)):
    return {
        "message": "Deleting user account by the admin",
        "task": "Deleting user account",
        "user": user,
    }
