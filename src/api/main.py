from fastapi import APIRouter

from src.api.routes import auth_router, tasks_router, users_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(tasks_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)
