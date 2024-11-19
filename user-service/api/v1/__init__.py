from fastapi import APIRouter

from .address import user_address_router
from .authentication import authentication_router
from .monitoring import monitoring_router
from .profile import user_profile_router
from .users import users_router

v1_router: APIRouter = APIRouter()
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(authentication_router, prefix="/auth")
v1_router.include_router(user_profile_router, prefix="/profile")
v1_router.include_router(user_address_router, prefix="/address")
