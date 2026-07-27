from typing import Union

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.platform.users.models import User
from app.platform.users.repository import UserRepository
from app.platform.users.schemas import UserCreate
from app.platform.users.schemas import UserUpdate
from app.shared.exceptions import ConflictException
from app.shared.exceptions import NotFoundException
from app.platform.tenants.models import Tenant

from uuid import UUID

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create(self, payload: UserCreate, creator: Union[Tenant, User]) -> User:
        if self.repository.get_by_email(payload.email):
            raise ConflictException("Email already exists.")

        # Tenant creates the first Agent
        if isinstance(creator, Tenant):
            tenant_id = creator.id
            parent_id = None
            role = "agent"

        # User hierarchy
        elif isinstance(creator, User):
            tenant_id = creator.tenant_id
            parent_id = creator.id

            if creator.role == "agent":
                role = "user"

            elif creator.role == "user":
                role = "intern"

            else:
                raise ConflictException(
                    "You are not allowed to create users."
                )

        else:
            raise ConflictException("Invalid creator.")

        user = User(
            tenant_id=tenant_id,
            parent_id=parent_id,
            role=role,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=pwd_context.hash(payload.password),
        )

        self.repository.add(user)

        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all(self):
        return self.repository.list()

    def get_by_uuid(self, uuid: UUID):
        user = self.repository.get_by_uuid(uuid)

        if not user:
            raise NotFoundException("User not found.")

        return user

    def update(self, uuid: UUID, payload: UserUpdate):
        user = self.get_by_uuid(uuid)

        data = payload.model_dump(exclude_unset=True)

        if "password" in data:
            data["hashed_password"] = pwd_context.hash(data.pop("password"))

        user = self.repository.update(user, data)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete(self, uuid: UUID):
        user = self.get_by_uuid(uuid)

        self.repository.delete(user)

        self.db.commit()