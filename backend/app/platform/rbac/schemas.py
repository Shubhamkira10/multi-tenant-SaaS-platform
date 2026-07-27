from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


# ------------------------------------------------------------------
# Feature → Tenant
# ------------------------------------------------------------------

class AssignFeatureToTenantRequest(BaseModel):
    tenant_uuid: UUID
    feature_uuid: UUID


class TenantFeatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    tenant_id: int
    feature_id: int
    is_enabled: bool


# ------------------------------------------------------------------
# Feature → User
# ------------------------------------------------------------------

class AssignFeatureToUserRequest(BaseModel):
    user_uuid: UUID
    feature_uuid: UUID


class UserFeatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    user_id: int
    feature_id: int
    assigned_by: int | None
    is_enabled: bool


# ------------------------------------------------------------------
# Permission → Feature
# ------------------------------------------------------------------

class AssignPermissionToFeatureRequest(BaseModel):
    feature_uuid: UUID
    permission_uuid: UUID


class FeaturePermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    feature_id: int
    permission_id: int


# ------------------------------------------------------------------
# Generic Feature Response
# ------------------------------------------------------------------

class FeatureSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    name: str
    slug: str
    route: str
    icon: str | None


class PermissionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    name: str
    slug: str


class FeatureWithPermissions(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    feature: FeatureSummary
    permissions: list[PermissionSummary]