from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_platform_admin
from app.platform.admins.models import PlatformAdmin
from app.shared.schemas import ApiResponse

from .schemas import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)
from .service import PermissionService

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[PermissionResponse],
)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(
        get_current_platform_admin
    ),
):

    permission = PermissionService(db).create(payload)

    return ApiResponse(
        message="Permission created successfully.",
        data=permission,
    )


@router.get(
    "",
    response_model=ApiResponse[list[PermissionResponse]],
)
def list_permissions(
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(
        get_current_platform_admin
    ),
):

    permissions = PermissionService(db).get_all()

    return ApiResponse(
        message="Permissions fetched successfully.",
        data=permissions,
    )


@router.get(
    "/{uuid}",
    response_model=ApiResponse[PermissionResponse],
)
def get_permission(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(
        get_current_platform_admin
    ),
):

    permission = PermissionService(db).get(uuid)

    return ApiResponse(
        message="Permission fetched successfully.",
        data=permission,
    )


@router.put(
    "/{uuid}",
    response_model=ApiResponse[PermissionResponse],
)
def update_permission(
    uuid: UUID,
    payload: PermissionUpdate,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(
        get_current_platform_admin
    ),
):

    permission = PermissionService(db).update(
        uuid,
        payload,
    )

    return ApiResponse(
        message="Permission updated successfully.",
        data=permission,
    )


@router.delete(
    "/{uuid}",
    response_model=ApiResponse[None],
)
def delete_permission(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(
        get_current_platform_admin
    ),
):

    PermissionService(db).delete(uuid)

    return ApiResponse(
        message="Permission deleted successfully.",
        data=None,
    )