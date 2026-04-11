import uuid
from datetime import datetime, date
from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class Project(Base):
  __tablename__ = "projects"
  __table_args__ = (
    CheckConstraint("min_session_time >= 0", name="ck_projects_min_session_time_non_negative"),
  )

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
  name: Mapped[str] = mapped_column(
    String(100),
    nullable=False
  )
  description: Mapped[str] = mapped_column(
    Text,
    nullable=True
  )
  due_date: Mapped[date] = mapped_column(
    Date,
    nullable=False
  )
  min_session_time: Mapped[int] = mapped_column(
    Integer,
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
