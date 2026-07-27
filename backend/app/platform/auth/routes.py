from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.schemas import ApiResponse
from app.core.dependencies import get_current_platform_admin
from app.platform.admins.models import PlatformAdmin


from .schemas import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from .service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/platform/login",
    response_model=ApiResponse[TokenResponse],
)
def platform_login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    tokens = AuthService(db).login_platform_admin(
        payload.email,
        payload.password,
    )

    return ApiResponse(
        message="Platform admin login successful.",
        data=tokens,
    )


@router.post(
    "/tenant/login",
    response_model=ApiResponse[TokenResponse],
)
def tenant_login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    tokens = AuthService(db).login_tenant(
        payload.email,
        payload.password,
    )

    return ApiResponse(
        message="Tenant login successful.",
        data=tokens,
    )

@router.post(
    "/user/login",
    response_model=ApiResponse[TokenResponse],
)
def user_login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    tokens = AuthService(db).login_user(
        payload.email,
        payload.password,
    )

    return ApiResponse(
        message="User login successful.",
        data=tokens,
    )


@router.post(
    "/refresh",
    response_model=ApiResponse[TokenResponse],
)
def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    tokens = AuthService(db).refresh_token(
        payload.refresh_token,
    )

    return ApiResponse(
        message="Token refreshed successfully.",
        data=tokens,
    )

