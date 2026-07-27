from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.shared.base_model import BaseModel

if TYPE_CHECKING:
    from app.platform.feature_permissions.models import FeaturePermission
    from app.platform.tenants.models import Tenant
    from app.platform.users.models import User


class Feature(BaseModel):
    __tablename__ = "features"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    route: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    icon: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    tenant_features: Mapped[list["TenantFeature"]] = relationship(
        back_populates="feature",
        cascade="all, delete-orphan",
    )

    user_features: Mapped[list["UserFeature"]] = relationship(
        back_populates="feature",
        cascade="all, delete-orphan",
    )

    feature_permissions: Mapped[list["FeaturePermission"]] = relationship(
        back_populates="feature",
        cascade="all, delete-orphan",
    )


class TenantFeature(BaseModel):
    __tablename__ = "tenant_features"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    feature_id: Mapped[int] = mapped_column(
        ForeignKey(
            "features.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    tenant: Mapped["Tenant"] = relationship(
        back_populates="tenant_features",
    )

    feature: Mapped["Feature"] = relationship(
        back_populates="tenant_features",
    )


class UserFeature(BaseModel):
    __tablename__ = "user_features"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    feature_id: Mapped[int] = mapped_column(
        ForeignKey(
            "features.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    assigned_by: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        back_populates="user_features",
    )

    assigned_by_user: Mapped["User | None"] = relationship(
        foreign_keys=[assigned_by],
    )

    feature: Mapped["Feature"] = relationship(
        back_populates="user_features",
    )