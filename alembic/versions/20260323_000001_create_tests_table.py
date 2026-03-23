"""create tests table

Revision ID: 20260323_000001
Revises:
Create Date: 2026-03-23 00:00:01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260323_000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_tests_id"), "tests", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tests_id"), table_name="tests")
    op.drop_table("tests")
