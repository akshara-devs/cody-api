from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.test import TestRecord
from schemas.test import TestCreate


def create_test_record(db: Session, payload: TestCreate) -> TestRecord:
    # Simple seed/example insert service for teammates to replace later.
    record = TestRecord(name=payload.name)
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Test record already exists.",
        ) from exc
    db.refresh(record)
    return record
