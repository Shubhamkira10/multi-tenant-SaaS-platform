from sqlalchemy import select
from sqlalchemy.orm import Session

from app.platform.users.models import User
from app.shared.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        return self.first(email=email)