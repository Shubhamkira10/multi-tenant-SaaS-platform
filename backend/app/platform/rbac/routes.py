from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_platform_admin,
    get_current_user,
)

from app.platform.users.models import User
from app.platform.admins.models import PlatformAdmin

from app.platform.rbac.schemas import (
    AssignFeatureToTenantRequest,
    AssignFeatureToUserRequest,
    AssignPermissionToFeatureRequest,
    TenantFeatureResponse,
    UserFeatureResponse,
    FeaturePermissionResponse,
)

from app.platform.rbac.service import RBACService

router = APIRouter(
    prefix="/rbac",
    tags=["RBAC"],
)


# ==========================================================
# Feature -> Tenant
# ==========================================================


@router.post(
    "/tenants/features",
    response_model=TenantFeatureResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_feature_to_tenant(
    payload: AssignFeatureToTenantRequest,
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    return service.assign_feature_to_tenant(
        tenant_uuid=payload.tenant_uuid,
        feature_uuid=payload.feature_uuid,
    )


@router.delete(
    "/tenants/{tenant_uuid}/features/{feature_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_feature_from_tenant(
    tenant_uuid: UUID,
    feature_uuid: UUID,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    service.remove_feature_from_tenant(
        tenant_uuid=tenant_uuid,
        feature_uuid=feature_uuid,
    )


@router.get(
    "/tenants/{tenant_uuid}/features",
    response_model=list[TenantFeatureResponse],
)
def get_tenant_features(
    tenant_uuid: UUID,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    return service.get_tenant_features(
        tenant_uuid=tenant_uuid,
    )


# ==========================================================
# Feature -> User
# ==========================================================

@router.post(
    "/users/features",
    response_model=UserFeatureResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_feature_to_user(
    payload: AssignFeatureToUserRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    return service.assign_feature_to_user(
        parent_uuid=current_user.uuid,
        user_uuid=payload.user_uuid,
        feature_uuid=payload.feature_uuid,
    )


@router.delete(
    "/users/{user_uuid}/features/{feature_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_feature_from_user(
    user_uuid: UUID,
    feature_uuid: UUID,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    service.remove_feature_from_user(
        user_uuid=user_uuid,
        feature_uuid=feature_uuid,
    )


@router.get(
    "/users/{user_uuid}/features",
    response_model=list[UserFeatureResponse],
)
def get_user_features(
    user_uuid: UUID,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    return service.get_user_features(
        user_uuid=user_uuid,
    )


# ==========================================================
# Feature -> Permission
# ==========================================================


@router.post(
    "/features/permissions",
    response_model=FeaturePermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_permission_to_feature(
    payload: AssignPermissionToFeatureRequest,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    return service.assign_permission_to_feature(
        feature_uuid=payload.feature_uuid,
        permission_uuid=payload.permission_uuid,
    )


@router.delete(
    "/features/{feature_uuid}/permissions/{permission_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_permission_from_feature(
    feature_uuid: UUID,
    permission_uuid: UUID,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    service.remove_permission_from_feature(
        feature_uuid=feature_uuid,
        permission_uuid=permission_uuid,
    )


@router.get(
    "/features/{feature_uuid}/permissions",
    response_model=list[FeaturePermissionResponse],
)
def get_feature_permissions(
    feature_uuid: UUID,
    db: Session = Depends(get_db),
):
    service = RBACService(db)

    return service.get_feature_permissions(
        feature_uuid=feature_uuid,
    )