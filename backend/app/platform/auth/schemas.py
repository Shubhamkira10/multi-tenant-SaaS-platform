from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class FeatureMenu(BaseModel):
    uuid: str
    name: str
    slug: str
    route: str
    icon: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    tenant_uuid: str | None = None
    tenant_name: str | None = None

    features: list[FeatureMenu] = []

class CurrentUserResponse(BaseModel):
    uuid: str
    email: EmailStr
    role: str | None = None
    tenant_id: int | None = None
    user_type: str