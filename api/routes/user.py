from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from db.session import get_db

from typing import Annotated
from schemas.user import UserCreate, UserResponse, UserDelete

from services.user_service import create_user, delete_user
from api.deps import verify_internal_api_key

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register_route(
  _: Annotated[None, Depends(verify_internal_api_key)],
  payload: Annotated[UserCreate, Body(...)],
  db: Session = Depends(get_db)
):
  return create_user(db, payload)

@router.delete("/delete", status_code=200)
def delete_route(
  _: Annotated[None, Depends(verify_internal_api_key)],
  payload: Annotated[UserDelete, Body(...)],
  db: Session = Depends(get_db)
):
  return delete_user(db, payload)