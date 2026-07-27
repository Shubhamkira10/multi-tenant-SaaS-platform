"""add hashed password to tenants

Revision ID: 0eb260cd85fd
Revises: 59f912ff14ee
Create Date: 2026-07-23 15:35:40.627239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb260cd85fd'
down_revision: Union[str, Sequence[str], None] = '59f912ff14ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "tenants",
        sa.Column("hashed_password", sa.String(length=255), nullable=False)
    )


def downgrade():
    op.drop_column("tenants", "hashed_password")
