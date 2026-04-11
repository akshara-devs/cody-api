from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserDelete

def create_user(db: Session, payload: UserCreate) -> User:
  record = User(discord_user_id=payload.discord_user_id)
  db.add(record)
  try:
    db.commit()
  except IntegrityError as exc:
    db.rollback()
    raise HTTPException(
      status_code=409,
      detail="User already exist.",
    ) from exc
  db.refresh(record)
  return record

def delete_user(db: Session, payload: UserDelete) -> str:
  record = db.query(User).filter(User.discord_user_id == payload.discord_user_id).first()
  if not record:
    raise HTTPException(
      status_code=409,
      detail="User not found.",
    )
  db.delete(record)
  try:
    db.commit()
  except IntegrityError as exc:
    db.rollback()
    raise HTTPException(
      status_code=500,
      detail="Failed to delete user.",
    ) from exc
  return "User deleted successfully."