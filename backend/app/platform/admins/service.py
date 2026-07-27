from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import pwd_context
from app.shared.exceptions import (
    ConflictException,
    NotFoundException,
)

from .models import PlatformAdmin
from .repository import PlatformAdminRepository
from .schemas import (
    PlatformAdminCreate,
    PlatformAdminUpdate,
)


class PlatformAdminService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PlatformAdminRepository(db)

    def create(self, payload: PlatformAdminCreate) -> PlatformAdmin:
        if self.repository.get_by_email(payload.email):
            raise ConflictException(
                "Platform admin with this email already exists."
            )

        admin = PlatformAdmin(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=pwd_context.hash(payload.password),
        )

        self.repository.add(admin)

        self.db.commit()
        self.db.refresh(admin)

        return admin

    def list(self) -> list[PlatformAdmin]:
        return self.repository.list()

    def get_by_uuid(self, uuid: UUID) -> PlatformAdmin:
        admin = self.repository.get_by_uuid(uuid)

        if not admin:
            raise NotFoundException("Platform admin not found.")

        return admin

    def update(
        self,
        uuid: UUID,
        payload: PlatformAdminUpdate,
    ) -> PlatformAdmin:
        admin = self.get_by_uuid(uuid)

        data = payload.model_dump(exclude_unset=True)

        if "password" in data:
            data["hashed_password"] = pwd_context.hash(data.pop("password"))

        self.repository.update(admin, data)

        self.db.commit()
        self.db.refresh(admin)

        return admin

    def delete(self, uuid: UUID) -> None:
        admin = self.get_by_uuid(uuid)

        self.repository.delete(admin)

        self.db.commit()