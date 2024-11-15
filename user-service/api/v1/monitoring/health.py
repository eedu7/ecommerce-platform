from fastapi import APIRouter

from app.schemas.extra.health import Health

health_router: APIRouter = APIRouter()


@health_router.get("/")
async def health() -> Health:
    return Health(version="1.0.0", status="Health")
