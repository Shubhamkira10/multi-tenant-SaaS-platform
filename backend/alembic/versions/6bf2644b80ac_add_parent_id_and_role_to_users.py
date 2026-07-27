"""add parent_id and role to users

Revision ID: 6bf2644b80ac
Revises: 0eb260cd85fd
Create Date: 2026-07-23 17:45:54.809494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6bf2644b80ac'
down_revision: Union[str, Sequence[str], None] = '0eb260cd85fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("users") as batch_op:

        batch_op.add_column(
            sa.Column(
                "parent_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "role",
                sa.String(length=50),
                nullable=False,
                server_default="user",
            )
        )

        batch_op.create_index(
            "ix_users_parent_id",
            ["parent_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            "fk_users_parent_id",
            "users",
            ["parent_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("users") as batch_op:

        batch_op.drop_constraint(
            "fk_users_parent_id",
            type_="foreignkey",
        )

        batch_op.drop_index(
            "ix_users_parent_id",
        )

        batch_op.drop_column("role")

        batch_op.drop_column("parent_id")