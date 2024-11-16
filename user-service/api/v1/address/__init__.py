from fastapi import APIRouter

from .address import address_router

user_address_router = APIRouter()
user_address_router.include_router(address_router, tags=["Address"])
