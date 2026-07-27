from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.platform.features.models import UserFeature

from app.platform.tenants.models import Tenant
from app.shared.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="user",
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )


    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    tenant: Mapped["Tenant"] = relationship(
        back_populates="users",
    )

    parent: Mapped["User | None"] = relationship(
        "User",
        remote_side="User.id",
        back_populates="children",
    )

    children: Mapped[list["User"]] = relationship(
        "User",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    user_features: Mapped[list["UserFeature"]] = relationship(
        foreign_keys="UserFeature.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )