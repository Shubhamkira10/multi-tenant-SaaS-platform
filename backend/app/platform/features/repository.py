from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.platform.features.models import (
    Feature,
    TenantFeature,
    UserFeature,
)
from app.shared.base_repository import BaseRepository


class FeatureRepository(BaseRepository[Feature]):
    def __init__(self, db: Session):
        super().__init__(Feature, db)

    # ------------------------------------------------------------------
    # Feature Operations
    # ------------------------------------------------------------------

    def get_by_slug(self, slug: str) -> Feature | None:
        stmt = select(Feature).where(Feature.slug == slug)
        return self.db.scalar(stmt)

    def slug_exists(self, slug: str) -> bool:
        return self.get_by_slug(slug) is not None

    def get_active_features(self) -> list[Feature]:
        stmt = (
            select(Feature)
            .where(Feature.is_active == True)
            .order_by(Feature.name)
        )
        return list(self.db.scalars(stmt).all())

    # ------------------------------------------------------------------
    # Tenant Feature Operations
    # ------------------------------------------------------------------

    def get_tenant_features(
        self,
        tenant_id: int,
    ) -> list[TenantFeature]:

        stmt = (
            select(TenantFeature)
            .where(
                TenantFeature.tenant_id == tenant_id,
                TenantFeature.is_enabled == True,
            )
        )

        return list(self.db.scalars(stmt).all())

    def get_tenant_feature_ids(
        self,
        tenant_id: int,
    ) -> set[int]:

        features = self.get_tenant_features(tenant_id)

        return {
            feature.feature_id
            for feature in features
        }

    # ------------------------------------------------------------------
    # User Feature Operations
    # ------------------------------------------------------------------

    def get_user_features(
        self,
        user_id: int,
    ) -> list[UserFeature]:

        stmt = (
            select(UserFeature)
            .where(
                UserFeature.user_id == user_id,
                UserFeature.is_enabled == True,
            )
        )

        return list(self.db.scalars(stmt).all())

    def get_user_feature_ids(
        self,
        user_id: int,
    ) -> set[int]:

        features = self.get_user_features(user_id)

        return {
            feature.feature_id
            for feature in features
        }

    # ------------------------------------------------------------------
    # Assignment Helpers
    # ------------------------------------------------------------------

    def assign_feature_to_tenant(
        self,
        tenant_id: int,
        feature_id: int,
    ) -> TenantFeature:

        assignment = TenantFeature(
            tenant_id=tenant_id,
            feature_id=feature_id,
            is_enabled=True,
        )

        self.db.add(assignment)

        return assignment

    def assign_feature_to_user(
        self,
        user_id: int,
        feature_id: int,
    ) -> UserFeature:

        assignment = UserFeature(
            user_id=user_id,
            feature_id=feature_id,
            is_enabled=True,
        )

        self.db.add(assignment)

        return assignment