from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


if not settings.database_url:
    raise ValueError("DATABASE_URL is not set.")


# Shared SQLAlchemy engine/session for the API.
engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
