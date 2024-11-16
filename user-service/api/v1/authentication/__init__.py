from fastapi import APIRouter

from .authentication import auth_router

authentication_router: APIRouter = APIRouter()
authentication_router.include_router(auth_router, tags=["Authentication"])

__all__ = ["authentication_router"]
