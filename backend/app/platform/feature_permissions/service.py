from __future__ import annotations

from sqlalchemy.orm import Session

from app.platform.feature_permissions.models import (
    FeaturePermission,
)
from app.platform.feature_permissions.repository import (
    FeaturePermissionRepository,
)
from app.shared.exceptions import (
    ConflictException,
)


class FeaturePermissionService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.repository = FeaturePermissionRepository(
            db
        )

    def assign_permission(
        self,
        feature_id: int,
        permission_id: int,
    ) -> FeaturePermission:

        if self.repository.exists(
            feature_id,
            permission_id,
        ):
            raise ConflictException(
                "Permission already assigned."
            )

        mapping = FeaturePermission(
            feature_id=feature_id,
            permission_id=permission_id,
        )

        self.repository.add(mapping)

        self.db.commit()
        self.db.refresh(mapping)

        return mapping

    def get_feature_permissions(
        self,
        feature_id: int,
    ):

        return self.repository.get_permissions_by_feature(
            feature_id
        )