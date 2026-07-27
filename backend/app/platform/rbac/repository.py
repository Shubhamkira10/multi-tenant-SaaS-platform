from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.platform.feature_permissions.models import FeaturePermission
from app.platform.features.models import (
    Feature,
    TenantFeature,
    UserFeature,
)
from app.platform.permissions.models import Permission
from app.platform.tenants.models import Tenant
from app.platform.users.models import User


class RBACRepository:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # Feature
    # ==========================================================

    def get_feature_by_uuid(
        self,
        uuid: UUID,
    ) -> Feature | None:

        stmt = (
            select(Feature)
            .where(Feature.uuid == uuid)
        )

        return self.db.scalar(stmt)

    # ==========================================================
    # Permission
    # ==========================================================

    def get_permission_by_uuid(
        self,
        uuid: UUID,
    ) -> Permission | None:

        stmt = (
            select(Permission)
            .where(Permission.uuid == uuid)
        )

        return self.db.scalar(stmt)

    # ==========================================================
    # Tenant
    # ==========================================================

    def get_tenant_by_uuid(
        self,
        uuid: UUID,
    ) -> Tenant | None:

        stmt = (
            select(Tenant)
            .where(Tenant.uuid == uuid)
        )

        return self.db.scalar(stmt)

    # ==========================================================
    # User
    # ==========================================================

    def get_user_by_uuid(
        self,
        uuid: UUID,
    ) -> User | None:

        stmt = (
            select(User)
            .where(User.uuid == uuid)
        )

        return self.db.scalar(stmt)

    # ==========================================================
    # Tenant Feature Assignment
    # ==========================================================

    def tenant_has_feature(
        self,
        tenant_id: int,
        feature_id: int,
    ) -> bool:

        stmt = (
            select(TenantFeature)
            .where(
                TenantFeature.tenant_id == tenant_id,
                TenantFeature.feature_id == feature_id,
            )
        )

        return self.db.scalar(stmt) is not None

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

    def remove_feature_from_tenant(
        self,
        tenant_id: int,
        feature_id: int,
    ) -> None:

        stmt = (
            select(TenantFeature)
            .where(
                TenantFeature.tenant_id == tenant_id,
                TenantFeature.feature_id == feature_id,
            )
        )

        assignment = self.db.scalar(stmt)

        if assignment:
            self.db.delete(assignment)

    def get_tenant_features(
        self,
        tenant_id: int,
    ) -> list[TenantFeature]:

        stmt = (
            select(TenantFeature)
            .options(
                joinedload(TenantFeature.feature)
            )
            .where(
                TenantFeature.tenant_id == tenant_id,
                TenantFeature.is_enabled == True,
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ==========================================================
    # User Feature Assignment
    # ==========================================================

    def user_has_feature(
        self,
        user_id: int,
        feature_id: int,
    ) -> bool:

        stmt = (
            select(UserFeature)
            .where(
                UserFeature.user_id == user_id,
                UserFeature.feature_id == feature_id,
            )
        )

        return self.db.scalar(stmt) is not None

    def assign_feature_to_user(
        self,
        user_id: int,
        feature_id: int,
        assigned_by: int,
    ) -> UserFeature:

        assignment = UserFeature(
            user_id=user_id,
            feature_id=feature_id,
            assigned_by=assigned_by,
            is_enabled=True,
        )

        self.db.add(assignment)

        return assignment

    def remove_feature_from_user(
        self,
        user_id: int,
        feature_id: int,
    ) -> None:

        stmt = (
            select(UserFeature)
            .where(
                UserFeature.user_id == user_id,
                UserFeature.feature_id == feature_id,
            )
        )

        assignment = self.db.scalar(stmt)

        if assignment:
            self.db.delete(assignment)

    def get_user_features(
        self,
        user_id: int,
    ) -> list[UserFeature]:

        stmt = (
            select(UserFeature)
            .options(
                joinedload(UserFeature.feature)
            )
            .where(
                UserFeature.user_id == user_id,
                UserFeature.is_enabled == True,
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ==========================================================
    # Feature Permission Assignment
    # ==========================================================

    def feature_has_permission(
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

    def assign_permission_to_feature(
        self,
        feature_id: int,
        permission_id: int,
    ) -> FeaturePermission:

        assignment = FeaturePermission(
            feature_id=feature_id,
            permission_id=permission_id,
        )

        self.db.add(assignment)

        return assignment

    def remove_permission_from_feature(
        self,
        feature_id: int,
        permission_id: int,
    ) -> None:

        stmt = (
            select(FeaturePermission)
            .where(
                FeaturePermission.feature_id == feature_id,
                FeaturePermission.permission_id == permission_id,
            )
        )

        assignment = self.db.scalar(stmt)

        if assignment:
            self.db.delete(assignment)

    def get_feature_permissions(
        self,
        feature_id: int,
    ) -> list[FeaturePermission]:

        stmt = (
            select(FeaturePermission)
            .options(
                joinedload(FeaturePermission.permission)
            )
            .where(
                FeaturePermission.feature_id == feature_id,
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )