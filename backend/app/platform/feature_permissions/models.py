from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.shared.base_model import BaseModel

if TYPE_CHECKING:
    from app.platform.features.models import Feature
    from app.platform.permissions.models import Permission


class FeaturePermission(BaseModel):
    __tablename__ = "feature_permissions"

    feature_id: Mapped[int] = mapped_column(
        ForeignKey(
            "features.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    feature: Mapped["Feature"] = relationship(
        back_populates="feature_permissions",
    )

    permission: Mapped["Permission"] = relationship(
        back_populates="feature_permissions",
    )

    __table_args__ = (
        UniqueConstraint(
            "feature_id",
            "permission_id",
            name="uq_feature_permission",
        ),
    )