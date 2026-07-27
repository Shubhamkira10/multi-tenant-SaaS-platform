from __future__ import annotations

from sqlalchemy.orm import Session

from app.platform.features.models import Feature
from app.platform.features.repository import FeatureRepository
from app.platform.features.schemas import (
    FeatureCreate,
    FeatureUpdate,
)

from app.shared.exceptions import (
    ConflictException,
    NotFoundException,
)

from app.shared.utils import generate_unique_slug


class FeatureService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = FeatureRepository(db)

    def create(self, payload: FeatureCreate) -> Feature:

        slug = generate_unique_slug(
            payload.name,
            self.repository.slug_exists,
        )

        if self.repository.slug_exists(slug):
            raise ConflictException("Feature already exists.")

        feature = Feature(
            name=payload.name,
            slug=slug,
            route=payload.route,
            icon=payload.icon,
            description=payload.description,
        )

        self.db.add(feature)
        self.db.commit()
        self.db.refresh(feature)

        return feature

    def get_all(self):

        return self.repository.get_active_features()

    def get_by_uuid(self, uuid):

        feature = self.repository.get_by_uuid(uuid)

        if not feature:
            raise NotFoundException("Feature not found.")

        return feature

    def update(
        self,
        uuid,
        payload: FeatureUpdate,
    ):

        feature = self.get_by_uuid(uuid)

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(feature, key, value)

        self.db.commit()
        self.db.refresh(feature)

        return feature

    def delete(self, uuid):

        feature = self.get_by_uuid(uuid)

        self.db.delete(feature)
        self.db.commit()

        return True