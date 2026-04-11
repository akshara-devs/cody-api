import uuid
import enum
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class TransactionType(enum.Enum):
  PURCHASE = "purchase"

class Transaction(Base):
  __tablename__ = "transactions"
  __table_args__ = (
    CheckConstraint("amount >= 0", name="ck_transactions_amount_non_negative"),
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
  item_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("items.id"),
    nullable=False
  )
  type: Mapped[TransactionType] = mapped_column(
    Enum(TransactionType, name="transaction_type"),
    nullable=False
  )
  amount: Mapped[int] = mapped_column(
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
