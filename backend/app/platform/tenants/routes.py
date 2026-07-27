from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_platform_admin
from app.platform.admins.models import PlatformAdmin


from app.shared.schemas import ApiResponse



from .schemas import (
    TenantCreate,
    TenantUpdate,
    TenantResponse,
)
from .service import TenantService

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[TenantResponse],
)
def create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    tenant = TenantService(db).create(payload)

    return ApiResponse(
        message="Tenant created successfully.",
        data=tenant,
    )

@router.get(
    "",
    response_model=ApiResponse[list[TenantResponse]],
)
def list_tenants(
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    tenants = TenantService(db).get_all()

    return ApiResponse(
        message="Tenants fetched successfully.",
        data=tenants,
    )

@router.get(
    "/{uuid}",
    response_model=ApiResponse[TenantResponse],
)
def get_tenant(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    tenant = TenantService(db).get(uuid)

    return ApiResponse(
        message="Tenant fetched successfully.",
        data=tenant,
    )

@router.put(
    "/{uuid}",
    response_model=ApiResponse[TenantResponse],
)
def update_tenant(
    uuid: UUID,
    payload: TenantUpdate,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    tenant = TenantService(db).update(uuid, payload)

    return ApiResponse(
        message="Tenant updated successfully.",
        data=tenant,
    )

@router.delete(
    "/{uuid}",
    response_model=ApiResponse[None],
)
def delete_tenant(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    TenantService(db).delete(uuid)

    return ApiResponse(
        message="Tenant deleted successfully.",
        data=None,
    )