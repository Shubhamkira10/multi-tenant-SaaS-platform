from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import decode_token

from app.platform.admins.models import PlatformAdmin
from app.platform.admins.repository import PlatformAdminRepository

from app.platform.tenants.models import Tenant
from app.platform.tenants.repository import TenantRepository

from app.platform.users.models import User
from app.platform.users.repository import UserRepository

from app.shared.exceptions import UnauthorizedException

security = HTTPBearer()

def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    return decode_token(token)

def get_current_platform_admin(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> PlatformAdmin:

    if payload.get("entity") != "platform_admin":
        raise UnauthorizedException("Platform admin authentication required.")


    sub = payload.get("sub")

    if not sub:
        raise UnauthorizedException("Invalid token.")
    print("SUB:", sub)
    print("TYPE:", type(sub))
    print("UUID TYPE:", type(UUID(sub)))

    admin = PlatformAdminRepository(db).get_by_uuid(UUID(sub))

    if admin is None:
        raise UnauthorizedException("Platform admin not found.")

    return admin

def get_current_tenant(
    payload=Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> Tenant:

    if payload.get("entity") != "tenant":
        raise UnauthorizedException("Tenant authentication required.")

    tenant = TenantRepository(db).get_by_uuid(
        UUID(payload["sub"])
    )

    if tenant is None:
        raise UnauthorizedException("Tenant not found.")

    return tenant

def get_current_user(
    payload=Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> User:

    if payload.get("entity") != "user":
        raise UnauthorizedException("User authentication required.")

    user = UserRepository(db).get_by_uuid(
        UUID(payload["sub"])
    )

    if user is None:
        raise UnauthorizedException("User not found.")

    return user