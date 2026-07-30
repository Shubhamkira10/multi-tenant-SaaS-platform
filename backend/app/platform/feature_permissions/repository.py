from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.platform.feature_permissions.models import FeaturePermission
from app.shared.base_repository import BaseRepository


class FeaturePermissionRepository(
    BaseRepository[FeaturePermission]
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            FeaturePermission,
            db,
        )

    def get_permissions_by_feature(
        self,
        feature_id: int,
    ) -> list[FeaturePermission]:

        stmt = (
            select(FeaturePermission)
            .where(
                FeaturePermission.feature_id == feature_id
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def exists(
        self,
        feature_id: int,
        permission_id: int,
    ) -> bool:

        stmt = (
            select(FeaturePermission)
            .where(
                FeaturePermission.feature_id == feature_id,
                FeaturePermission.permission_id == permission_id,
            )
        )

        return self.db.scalar(stmt) is not None