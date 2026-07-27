from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.platform.tenants.models import Tenant
from app.shared.base_repository import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    def __init__(self, db: Session):
        super().__init__(Tenant, db)

    def get_by_slug(self, slug: str) -> Tenant | None:
        stmt = select(Tenant).where(Tenant.slug == slug)
        return self.db.scalar(stmt)

    def get_by_email(self, email: str) -> Tenant | None:
        return self.first(email=email)
    
    def slug_exists(self, slug: str) -> bool:
        return self.get_by_slug(slug) is not None