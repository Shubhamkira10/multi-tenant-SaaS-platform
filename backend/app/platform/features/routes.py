from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_platform_admin
from app.platform.admins.models import PlatformAdmin
from app.shared.schemas import ApiResponse

from .schemas import (
    FeatureCreate,
    FeatureUpdate,
    FeatureResponse,
)
from .service import FeatureService

router = APIRouter(
    prefix="/features",
    tags=["Features"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[FeatureResponse],
)
def create_feature(
    payload: FeatureCreate,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    feature = FeatureService(db).create(payload)

    return ApiResponse(
        message="Feature created successfully.",
        data=feature,
    )


@router.get(
    "",
    response_model=ApiResponse[list[FeatureResponse]],
)
def list_features(
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    features = FeatureService(db).get_all()

    return ApiResponse(
        message="Features fetched successfully.",
        data=features,
    )


@router.get(
    "/{uuid}",
    response_model=ApiResponse[FeatureResponse],
)
def get_feature(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    feature = FeatureService(db).get_by_uuid(uuid)

    return ApiResponse(
        message="Feature fetched successfully.",
        data=feature,
    )


@router.put(
    "/{uuid}",
    response_model=ApiResponse[FeatureResponse],
)
def update_feature(
    uuid: UUID,
    payload: FeatureUpdate,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    feature = FeatureService(db).update(
        uuid,
        payload,
    )

    return ApiResponse(
        message="Feature updated successfully.",
        data=feature,
    )


@router.delete(
    "/{uuid}",
    response_model=ApiResponse[None],
)
def delete_feature(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_admin: PlatformAdmin = Depends(get_current_platform_admin),
):
    FeatureService(db).delete(uuid)

    return ApiResponse(
        message="Feature deleted successfully.",
        data=None,
    )