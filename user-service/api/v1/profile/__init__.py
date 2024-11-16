from fastapi import APIRouter

from .profile import profile_router

user_profile_router: APIRouter = APIRouter()
user_profile_router.include_router(profile_router, tags=["Profile Management"])
