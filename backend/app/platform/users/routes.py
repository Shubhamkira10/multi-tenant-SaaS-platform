from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Union

from app.core.database import get_db
from app.platform.users.schemas import UserCreate
from app.platform.users.schemas import UserResponse
from app.platform.users.schemas import UserUpdate
from app.platform.users.service import UserService
from app.shared.schemas import ApiResponse
from app.core.dependencies import get_current_tenant
from app.core.dependencies import get_current_user
from app.platform.tenants.models import Tenant
from app.platform.users.models import User

from uuid import UUID 

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Tenant creates Agent
@router.post(
    "/agents",
    response_model=ApiResponse[UserResponse],
)
def create_agent(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant),
):
    user = UserService(db).create(
        payload,
        current_tenant,
    )

    return ApiResponse(
        success=True,
        message="Agent created successfully.",
        data=UserResponse.model_validate(user),
    )


# Agent/User creates User/Intern
@router.post(
    "",
    response_model=ApiResponse[UserResponse],
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = UserService(db).create(
        payload,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="User created successfully.",
        data=UserResponse.model_validate(user),
    )


@router.get("", response_model=ApiResponse[list[UserResponse]])
def get_users(
    db: Session = Depends(get_db),
):
    users = UserService(db).get_all()

    return ApiResponse(
        success=True,
        message="Users fetched successfully.",
        data=[UserResponse.model_validate(user) for user in users],
    )


@router.get("/{uuid}", response_model=ApiResponse[UserResponse])
def get_user(
    uuid: UUID,
    db: Session = Depends(get_db),
):
    user = UserService(db).get_by_uuid(uuid)

    return ApiResponse(
        success=True,
        message="User fetched successfully.",
        data=UserResponse.model_validate(user),
    )


@router.put("/{uuid}", response_model=ApiResponse[UserResponse])
def update_user(
    uuid: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    user = UserService(db).update(uuid, payload)

    return ApiResponse(
        success=True,
        message="User updated successfully.",
        data=UserResponse.model_validate(user),
    )


@router.delete("/{uuid}", response_model=ApiResponse[None])
def delete_user(
    uuid: UUID,
    db: Session = Depends(get_db),
):
    UserService(db).delete(uuid)

    return ApiResponse(
        success=True,
        message="User deleted successfully.",
    )