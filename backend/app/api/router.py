from fastapi import APIRouter

from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.platform.tenants.routes import router as tenant_router
from app.api.tenant import router as tenant_upload_router
from app.platform.users.routes import router as users_router
from app.platform.admins.routes import router as admin_router
from app.platform.auth.routes import router as auth_router
from app.platform.rbac.routes import router as rbac_router
from app.platform.features.routes import router as feature_router
from app.platform.permissions.routes import router as permission_router

api_router = APIRouter()

# System Routes
api_router.include_router(dashboard_router)
api_router.include_router(health_router)

# Tenant APIs
api_router.include_router(tenant_upload_router)

# Platform Routes
api_router.include_router(tenant_router)
api_router.include_router(users_router)
api_router.include_router(admin_router)
api_router.include_router(auth_router)

# RBAC Master Data
api_router.include_router(feature_router)
api_router.include_router(permission_router)

# RBAC Assignments
api_router.include_router(rbac_router)