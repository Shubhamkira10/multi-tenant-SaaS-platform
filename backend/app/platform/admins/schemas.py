from pydantic import BaseModel, EmailStr
from uuid import UUID

class PlatformAdminCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class PlatformAdminUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None


class PlatformAdminResponse(BaseModel):
    uuid: UUID
    full_name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }