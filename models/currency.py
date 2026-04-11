import uuid
import enum
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class CurrencyType(enum.Enum):
  GOLD = "gold"
  SILVER = "silver"
  DIAMOND = "diamond"

class Currency(Base):
  __tablename__ = "currencies"
  __table_args__ = (
    CheckConstraint("amount >= 0", name="ck_currencies_amount_non_negative"),
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
  amount: Mapped[int] = mapped_column(
    Integer,
    nullable=False
  )
  type: Mapped[CurrencyType] = mapped_column(
    Enum(CurrencyType, name="currency_type"),
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
