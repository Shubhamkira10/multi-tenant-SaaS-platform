from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.platform.permissions.models import Permission
from app.platform.permissions.repository import PermissionRepository
from app.platform.permissions.schemas import (
    PermissionCreate,
    PermissionUpdate,
)
from app.shared.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.shared.utils import generate_unique_slug


class PermissionService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = PermissionRepository(db)

    def create(
        self,
        payload: PermissionCreate,
    ) -> Permission:

        slug = generate_unique_slug(
            payload.name,
            self.repository.slug_exists,
        )

        permission = Permission(
            name=payload.name,
            slug=slug,
            description=payload.description,
        )

        self.repository.add(permission)

        try:
            self.db.commit()
            self.db.refresh(permission)
        except IntegrityError:
            self.db.rollback()
            raise ConflictException(
                "Permission already exists."
            )

        return permission

    def get_all(self):

        return self.repository.get_active_permissions()

    def get(
        self,
        uuid,
    ):

        permission = self.repository.get_by_uuid(uuid)

        if permission is None:
            raise NotFoundException(
                "Permission not found."
            )

        return permission

    def update(
        self,
        uuid,
        payload: PermissionUpdate,
    ):

        permission = self.get(uuid)

        update_data = payload.model_dump(
            exclude_unset=True,
        )

        self.repository.update(
            permission,
            update_data,
        )

        self.db.commit()
        self.db.refresh(permission)

        return permission

    def delete(
        self,
        uuid,
    ):

        permission = self.get(uuid)

        self.repository.delete(permission)

        self.db.commit()