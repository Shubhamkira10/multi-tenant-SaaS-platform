from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.platform.tenants.models import Tenant
from app.platform.tenants.service import TenantService
from app.shared.schemas import ApiResponse

router = APIRouter(
    prefix="/tenant",
    tags=["Tenant"],
)


@router.post(
    "/upload-data",
    response_model=ApiResponse[None],
)
async def upload_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    TenantService(db).upload_data(
        current_tenant.uuid,
        file,
    )

    return ApiResponse(
        message="Tenant data uploaded successfully.",
        data=None,
    )

@router.get(
    "/me",
    response_model=ApiResponse[dict],
)
def get_current_tenant_details(
    current_tenant: Tenant = Depends(get_current_tenant),
):
    return ApiResponse(
        message="Tenant details fetched successfully.",
        data={
            "uuid": str(current_tenant.uuid),
            "name": current_tenant.name,
            "email": current_tenant.email,
        },
    )