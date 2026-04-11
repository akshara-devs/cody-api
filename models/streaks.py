import uuid
from datetime import datetime, date
from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class Streak(Base):
  __tablename__ = "streaks"
  __table_args__ = (
    CheckConstraint("current_streak >= 0", name="ck_streaks_current_streak_non_negative"),
    CheckConstraint("longest_streak >= 0", name="ck_streaks_longest_streak_non_negative"),
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
  current_streak: Mapped[int] = mapped_column(
    Integer,
    default=0,
    nullable=False
  )
  last_active_date: Mapped[date] = mapped_column(
    Date,
    nullable=True
  )
  longest_streak: Mapped[int] = mapped_column(
    Integer,
    default=0,
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
