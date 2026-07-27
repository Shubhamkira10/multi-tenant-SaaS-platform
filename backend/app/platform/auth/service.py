from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)

from app.shared.exceptions import (
    NotFoundException,
    UnauthorizedException,
)

from app.platform.admins.repository import PlatformAdminRepository
from app.platform.users.repository import UserRepository
from app.platform.tenants.repository import TenantRepository
from app.platform.rbac.repository import RBACRepository

from .schemas import TokenResponse

class AuthService:

    def __init__(self, db):
        self.db = db
        self.admin_repository = PlatformAdminRepository(db)
        self.tenant_repository = TenantRepository(db)
        self.user_repository = UserRepository(db)
        self.rbac_repository = RBACRepository(db)

    def login_platform_admin(
        self,
        email: str,
        password: str,
    ) -> TokenResponse:

        admin = self.admin_repository.get_by_email(email)

        if not admin:
            raise UnauthorizedException("Invalid email or password.")

        if not verify_password(password, admin.hashed_password):
            raise UnauthorizedException("Invalid email or password.")

        payload = {
            "sub": str(admin.uuid),
            "entity": "platform_admin",
            "role": admin.role,
        }

        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload),
        )
    
    def login_tenant(
        self,
        email: str,
        password: str,
    ) -> TokenResponse:

        tenant = self.tenant_repository.get_by_email(email)

        if tenant is None:
            raise UnauthorizedException("Invalid email or password.")

        if not verify_password(password, tenant.hashed_password):
            raise UnauthorizedException("Invalid email or password.")

        payload = {
            "sub": str(tenant.uuid),
            "entity": "tenant",
        }

        tenant_features = self.rbac_repository.get_tenant_features(
            tenant.id
        )

        features = [
            {
                "uuid": str(item.feature.uuid),
                "name": item.feature.name,
                "slug": item.feature.slug,
                "route": item.feature.route,
                "icon": item.feature.icon or "",
            }
            for item in tenant_features
        ]

        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload),
            tenant_uuid=str(tenant.uuid),
            tenant_name=tenant.name,
            features=features,
        )

    def login_user(
        self,
        email: str,
        password: str,
    ) -> TokenResponse:

        user = self.user_repository.get_by_email(email)

        if not user:
            raise UnauthorizedException("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")

        payload = {
            "sub": str(user.uuid),
            "entity": "user",
            "tenant_id": user.tenant_id,
        }

        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload),
        )

    def refresh_token(
        self,
        refresh_token: str,
    ) -> TokenResponse:

        payload = decode_token(refresh_token)

        if payload.get("token_type") != "refresh":
            raise UnauthorizedException("Invalid refresh token.")

        new_payload = payload.copy()

        new_payload.pop("exp", None)
        new_payload.pop("token_type", None)

        return TokenResponse(
            access_token=create_access_token(new_payload),
            refresh_token=create_refresh_token(new_payload),
        )