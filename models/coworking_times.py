import uuid
import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class CoworkingType(enum.Enum):
  COWORKING = "coworking"
  BREAK = "break"
  EATING = "eating"
  DISTRACTED = "distracted"

class CoworkingTime(Base):
  __tablename__ = "coworking_times"

  id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4
  )
  user_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False
  )
  project_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("projects.id"),
    nullable=False
  )
  start_time: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    nullable=False
  )
  end_time: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    nullable=False
  )
  type: Mapped[CoworkingType] = mapped_column(
    Enum(CoworkingType, name="coworking_type"),
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
