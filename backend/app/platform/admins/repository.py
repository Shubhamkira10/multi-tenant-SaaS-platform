from app.shared.base_repository import BaseRepository

from .models import PlatformAdmin


class PlatformAdminRepository(BaseRepository[PlatformAdmin]):
    def __init__(self, db):
        super().__init__(PlatformAdmin, db)

    def get_by_email(self, email: str):
        return self.first(email=email)