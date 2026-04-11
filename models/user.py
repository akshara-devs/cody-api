import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class User(Base):
  __tablename__ = "users"

  id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True, 
    default=uuid.uuid4,
  )
  discord_user_id: Mapped[str] = mapped_column(
    String(21),
    unique=True,
    nullable=False
  )
  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    nullable=False
  )
  modified_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    onupdate=datetime.now,
    nullable=False
  )
