from fastapi import APIRouter

from api.routes.test import router as test_router
from api.routes.user import router as user_router

api_router = APIRouter()
api_router.include_router(test_router, prefix="/tests", tags=["tests"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
