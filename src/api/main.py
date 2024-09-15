from fastapi import APIRouter

from src.api.routes.items import router as items_router
from src.api.routes.tasks import tasks_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(items_router)
api_router.include_router(tasks_router)
