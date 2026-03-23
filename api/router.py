from fastapi import APIRouter

from api.routes.test import router as test_router


api_router = APIRouter()
api_router.include_router(test_router, prefix="/tests", tags=["tests"])
