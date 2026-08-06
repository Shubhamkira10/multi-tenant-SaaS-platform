"""add sender and reply email

Revision ID: 3a319143b0e7
Revises: 8f0be4bfebe3
Create Date: 2026-08-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision = "3a319143b0e7"
down_revision = "8f0be4bfebe3"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "tenants",
        sa.Column("sender_name", sa.String(255), nullable=True),
    )

    op.add_column(
        "tenants",
        sa.Column("reply_to_mail", sa.String(255), nullable=True),
    )


def downgrade():

    op.drop_column("tenants", "reply_to_mail")
    op.drop_column("tenants", "sender_name")