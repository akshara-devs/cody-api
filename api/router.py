from fastapi import APIRouter, FastAPI

from api.routes.test import router as test_router
from api.routes.user import router as user_router
from api.routes.project import router as project_router

api_router = APIRouter()
api_router.include_router(test_router, prefix="/tests", tags=["tests"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(project_router, prefix="/project", tags=["project"])