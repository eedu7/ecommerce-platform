from fastapi import APIRouter

from app.schemas.extras.health import Health
from core.config import config

health_router: APIRouter = APIRouter()


@health_router.get("/")
async def health() -> Health:
    return Health(version=config.VERSION, status="Health")
