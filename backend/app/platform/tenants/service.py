from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.platform.tenants.models import Tenant
from app.platform.tenants.repository import TenantRepository
from app.platform.tenants.schemas import TenantCreate, TenantUpdate
from app.shared.exceptions import ConflictException, NotFoundException
from app.shared.utils import slugify, generate_unique_slug
from app.core.security import hash_password
from app.platform.rbac.repository import RBACRepository

class TenantService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TenantRepository(db)
        self.rbac_repository = RBACRepository(db)

    def create(self, payload: TenantCreate) -> Tenant:

        if self.repository.get_by_email(payload.email):
            raise ConflictException("Email already exists.")

        slug = generate_unique_slug(
            payload.name,
            self.repository.slug_exists,
        )

        hashed_password = hash_password(payload.password)

        tenant = Tenant(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed_password,
            phone=payload.phone,
            description=payload.description,
            slug=slug,
        )

        self.repository.add(tenant)

        try:

            self.db.flush()

            for feature_uuid in payload.feature_uuids:

                feature = self.rbac_repository.get_feature_by_uuid(feature_uuid)

                if feature is None:
                    raise NotFoundException(
                        f"Feature {feature_uuid} not found."
                    )

                if not self.rbac_repository.tenant_has_feature(
                    tenant.id,
                    feature.id,
                ):
                    self.rbac_repository.assign_feature_to_tenant(
                        tenant.id,
                        feature.id,
                    )

            self.db.commit()
            self.db.refresh(tenant)

        except IntegrityError:

            self.db.rollback()
            raise ConflictException("Unable to create tenant.")

        return tenant

    def get_all(self) -> list[Tenant]:
        return self.repository.list()

    def get(self, uuid):
        tenant = self.repository.get_by_uuid(uuid)

        if tenant is None:
            raise NotFoundException("Tenant not found.")

        return tenant

    def update(self, uuid, payload: TenantUpdate) -> Tenant:
        tenant = self.get(uuid)

        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            if update_data["name"] != tenant.name:
                update_data["slug"] = generate_unique_slug(
                    update_data["name"],
                    self.repository.slug_exists,
                )

        for key, value in update_data.items():
            setattr(tenant, key, value)

        try:
            self.db.commit()
            self.db.refresh(tenant)
        except IntegrityError:
            self.db.rollback()
            raise ConflictException("Unable to update tenant.")

        return tenant

    def delete(self, uuid) -> None:
        tenant = self.get(uuid)
        self.repository.delete(tenant)
        self.db.commit()
    