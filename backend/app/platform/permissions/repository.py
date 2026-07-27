from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.platform.permissions.models import Permission
from app.shared.base_repository import BaseRepository


class PermissionRepository(BaseRepository[Permission]):

    def __init__(self, db: Session):
        super().__init__(Permission, db)

    def get_by_slug(
        self,
        slug: str,
    ) -> Permission | None:

        stmt = select(Permission).where(
            Permission.slug == slug
        )

        return self.db.scalar(stmt)

    def slug_exists(
        self,
        slug: str,
    ) -> bool:

        return self.get_by_slug(slug) is not None

    def get_active_permissions(
        self,
    ) -> list[Permission]:

        stmt = (
            select(Permission)
            .where(
                Permission.is_active == True
            )
            .order_by(
                Permission.name
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )