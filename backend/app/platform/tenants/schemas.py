from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class TenantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr

    password: str = Field(min_length=8)

    phone: str | None = None
    description: str | None = None

    feature_uuids: list[UUID] = Field(default_factory=list)

    support_email: EmailStr | None = None
    sender_name: str | None = None
    reply_to_email: EmailStr | None = None

class TenantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = None
    description: str | None = None
    is_active: bool | None = None
    support_email: EmailStr | None = None
    sender_name: str | None = None
    reply_to_email: EmailStr | None = None

class TenantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    name: str
    slug: str
    email: EmailStr
    phone: str | None
    description: str | None
    is_active: bool
    support_email: EmailStr | None = None
    sender_name: str | None = None
    reply_to_email: EmailStr | None = None