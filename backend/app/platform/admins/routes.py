from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.schemas import ApiResponse
from app.core.dependencies import get_current_platform_admin
from app.platform.admins.models import PlatformAdmin

from .schemas import (
    PlatformAdminCreate,
    PlatformAdminUpdate,
    PlatformAdminResponse,
)
from .service import PlatformAdminService

router = APIRouter(
    prefix="/platform-admins",
    tags=["Platform Admins"],
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[PlatformAdminResponse],
)
def create_platform_admin(
    payload: PlatformAdminCreate,
    db: Session = Depends(get_db),
):
    admin = PlatformAdminService(db).create(payload)

    return ApiResponse(
        message="Platform admin created successfully.",
        data=admin,
    )


@router.get(
    "",
    response_model=ApiResponse[list[PlatformAdminResponse]],
)
def list_platform_admins(
    db: Session = Depends(get_db),
):
    admins = PlatformAdminService(db).list()

    return ApiResponse(
        message="Platform admins fetched successfully.",
        data=admins,
    )


@router.get(
    "/{uuid}",
    response_model=ApiResponse[PlatformAdminResponse],
)
def get_platform_admin(
    uuid: UUID,
    db: Session = Depends(get_db),
):
    admin = PlatformAdminService(db).get_by_uuid(uuid)

    return ApiResponse(
        message="Platform admin fetched successfully.",
        data=admin,
    )


@router.put(
    "/{uuid}",
    response_model=ApiResponse[PlatformAdminResponse],
)
def update_platform_admin(
    uuid: UUID,
    payload: PlatformAdminUpdate,
    db: Session = Depends(get_db),
):
    admin = PlatformAdminService(db).update(uuid, payload)

    return ApiResponse(
        message="Platform admin updated successfully.",
        data=admin,
    )


@router.delete(
    "/{uuid}",
    response_model=ApiResponse[None],
)
def delete_platform_admin(
    uuid: UUID,
    db: Session = Depends(get_db),
):
    PlatformAdminService(db).delete(uuid)

    return ApiResponse(
        message="Platform admin deleted successfully.",
        data=None,
    )