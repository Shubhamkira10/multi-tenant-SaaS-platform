from __future__ import annotations

from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.platform.rbac.repository import RBACRepository
from app.platform.feature_permissions.models import FeaturePermission
from app.platform.features.models import (
    Feature,
    TenantFeature,
    UserFeature,
)
from app.platform.permissions.models import Permission
from app.platform.tenants.models import Tenant
from app.platform.users.models import User

from app.shared.exceptions import (
    ConflictException,
    NotFoundException,
    ForbiddenException,
)


class RBACService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = RBACRepository(db)

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _get_feature(
        self,
        feature_uuid: UUID,
    ) -> Feature:

        feature = self.repository.get_feature_by_uuid(
            feature_uuid
        )

        if feature is None:
            raise NotFoundException(
                "Feature not found."
            )

        return feature

    def _get_permission(
        self,
        permission_uuid: UUID,
    ) -> Permission:

        permission = self.repository.get_permission_by_uuid(
            permission_uuid
        )

        if permission is None:
            raise NotFoundException(
                "Permission not found."
            )

        return permission

    def _get_tenant(
        self,
        tenant_uuid: UUID,
    ) -> Tenant:

        tenant = self.repository.get_tenant_by_uuid(
            tenant_uuid
        )

        if tenant is None:
            raise NotFoundException(
                "Tenant not found."
            )

        return tenant

    def _get_user(
        self,
        user_uuid: UUID,
    ) -> User:

        user = self.repository.get_user_by_uuid(
            user_uuid
        )

        if user is None:
            raise NotFoundException(
                "User not found."
            )

        return user
    
    # ==========================================================
    # Feature -> Tenant
    # ==========================================================

    def assign_feature_to_tenant(
        self,
        tenant_uuid: UUID,
        feature_uuid: UUID,
    ) -> TenantFeature:

        tenant = self._get_tenant(
            tenant_uuid
        )

        feature = self._get_feature(
            feature_uuid
        )

        if self.repository.tenant_has_feature(
            tenant.id,
            feature.id,
        ):
            raise ConflictException(
                "Feature already assigned to tenant."
            )

        assignment = self.repository.assign_feature_to_tenant(
            tenant.id,
            feature.id,
        )

        try:
            self.db.commit()
            self.db.refresh(assignment)

        except IntegrityError as exc:

            self.db.rollback()

            raise ConflictException(
                "Unable to assign feature."
            )  from exc

        return assignment

    def remove_feature_from_tenant(
        self,
        tenant_uuid: UUID,
        feature_uuid: UUID,
    ) -> None:

        tenant = self._get_tenant(
            tenant_uuid
        )

        feature = self._get_feature(
            feature_uuid
        )

        self.repository.remove_feature_from_tenant(
            tenant.id,
            feature.id,
        )

        self.db.commit()

    def get_tenant_features(
        self,
        tenant_uuid: UUID,
    ) -> list[TenantFeature]:

        tenant = self._get_tenant(
            tenant_uuid
        )

        return self.repository.get_tenant_features(
            tenant.id
        )
    
    # ==========================================================
    # Feature -> User
    # ==========================================================

    def _user_has_feature(
        self,
        user_id: int,
        feature_id: int,
    ) -> bool:

        return self.repository.user_has_feature(
            user_id,
            feature_id,
        )

    def _validate_parent_assignment(
        self,
        parent: User,
        feature: Feature,
    ) -> None:

        # Platform Admin can assign everything
        if parent.tenant_id is None:
            return

        if not self._user_has_feature(
            parent.id,
            feature.id,
        ):
            raise ForbiddenException(
                "You cannot assign a feature that you do not have."
            )

    def _validate_user_hierarchy(
        self,
        parent: User,
        child: User,
    ) -> None:

        # Platform Admin
        if parent.tenant_id is None:
            return

        # Direct child validation
        if child.parent_id != parent.id:
            raise ForbiddenException(
                "You can only manage your direct child users."
            )

    def assign_feature_to_user(
        self,
        parent_uuid: UUID,
        user_uuid: UUID,
        feature_uuid: UUID,
    ) -> UserFeature:

        parent = self._get_user(parent_uuid)

        user = self._get_user(user_uuid)

        feature = self._get_feature(feature_uuid)

        # Prevent cross-tenant assignments
        if parent.tenant_id != user.tenant_id:
            raise ForbiddenException(
                "Users belong to different tenants."
            )
        
        self._validate_user_hierarchy(
            parent,
            user,
        )

        # Parent can only assign his own features
        self._validate_parent_assignment(
            parent,
            feature,
        )

        if self._user_has_feature(
            user.id,
            feature.id,
        ):
            raise ConflictException(
                "Feature already assigned."
            )

        assignment = self.repository.assign_feature_to_user(
            user.id,
            feature.id,
            parent.id,
        )

        try:

            self.db.commit()

            self.db.refresh(
                assignment
            )

        except IntegrityError as exc:

            self.db.rollback()

            raise ConflictException(
                "Unable to assign feature."
            ) from exc

        return assignment

    def remove_feature_from_user(
        self,
        user_uuid: UUID,
        feature_uuid: UUID,
    ) -> None:

        user = self._get_user(
            user_uuid
        )

        feature = self._get_feature(
            feature_uuid
        )

        self.repository.remove_feature_from_user(
            user.id,
            feature.id,
        )

        self.db.commit()

    def get_user_features(
        self,
        user_uuid: UUID,
    ) -> list[UserFeature]:

        user = self._get_user(
            user_uuid
        )

        return self.repository.get_user_features(
            user.id
        )
    
    # ==========================================================
    # Feature -> Permission
    # ==========================================================

    def assign_permission_to_feature(
        self,
        feature_uuid: UUID,
        permission_uuid: UUID,
    ) -> FeaturePermission:

        feature = self._get_feature(
            feature_uuid
        )

        permission = self._get_permission(
            permission_uuid
        )

        if self.repository.feature_has_permission(
            feature.id,
            permission.id,
        ):
            raise ConflictException(
                "Permission already assigned to feature."
            )

        assignment = self.repository.assign_permission_to_feature(
            feature.id,
            permission.id,
        )

        try:

            self.db.commit()

            self.db.refresh(
                assignment
            )

        except IntegrityError as exc:

            self.db.rollback()

            raise ConflictException(
                "Unable to assign permission."
            )  from exc

        return assignment

    def remove_permission_from_feature(
        self,
        feature_uuid: UUID,
        permission_uuid: UUID,
    ) -> None:

        feature = self._get_feature(
            feature_uuid
        )

        permission = self._get_permission(
            permission_uuid
        )

        self.repository.remove_permission_from_feature(
            feature.id,
            permission.id,
        )

        self.db.commit()

    def get_feature_permissions(
        self,
        feature_uuid: UUID,
    ) -> list[FeaturePermission]:

        feature = self._get_feature(
            feature_uuid
        )

        return self.repository.get_feature_permissions(
            feature.id
        )

    # ==========================================================
    # Utility Methods
    # ==========================================================

    def feature_exists(
        self,
        feature_uuid: UUID,
    ) -> bool:

        return (
            self.repository.get_feature_by_uuid(
                feature_uuid
            )
            is not None
        )

    def permission_exists(
        self,
        permission_uuid: UUID,
    ) -> bool:

        return (
            self.repository.get_permission_by_uuid(
                permission_uuid
            )
            is not None
        )

    def tenant_exists(
        self,
        tenant_uuid: UUID,
    ) -> bool:

        return (
            self.repository.get_tenant_by_uuid(
                tenant_uuid
            )
            is not None
        )

    def user_exists(
        self,
        user_uuid: UUID,
    ) -> bool:

        return (
            self.repository.get_user_by_uuid(
                user_uuid
            )
            is not None
        )
    