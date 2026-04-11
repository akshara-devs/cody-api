from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from db.session import get_db

from typing import Annotated
from schemas.test import TestCreate, TestResponse

from services.test_service import create_test_record


router = APIRouter()


@router.post("", response_model=TestResponse, status_code=201)
def create_test_route(
    payload: Annotated[TestCreate, Body(...)],
    db: Session = Depends(get_db),
):
    return create_test_record(db, payload)
