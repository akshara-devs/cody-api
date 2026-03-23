from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class TestRecord(Base):
    # Neutral example table so the project can serve as starter scaffolding.
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
