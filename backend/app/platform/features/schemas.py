from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class FeatureCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    route: str = Field(min_length=1, max_length=255)
    icon: str | None = None
    description: str | None = None


class FeatureUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    route: str | None = None
    icon: str | None = None
    description: str | None = None
    is_active: bool | None = None


class FeatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    name: str
    slug: str
    route: str
    icon: str | None
    description: str | None
    is_active: bool