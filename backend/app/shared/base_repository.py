from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository for common database operations.

    Responsibilities:
        - CRUD operations
        - Query helpers

    Transaction management (commit/rollback) is handled by the service layer.
    """

    def __init__(self, model: type[ModelType], db: Session) -> None:
        self.model = model
        self.db = db

    def add(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        return obj

    def get_by_id(self, id: int) -> ModelType | None:
        return self.db.get(self.model, id)

    def get_by_uuid(self, uuid: UUID) -> ModelType | None:
        stmt = select(self.model).where(self.model.uuid == uuid)
        return self.db.scalar(stmt)

    def list(self) -> list[ModelType]:
        stmt = select(self.model)
        return list(self.db.scalars(stmt).all())

    def filter_by(self, **filters: Any) -> list[ModelType]:
        stmt = select(self.model).filter_by(**filters)
        return list(self.db.scalars(stmt).all())

    def first(self, **filters: Any) -> ModelType | None:
        stmt = select(self.model).filter_by(**filters)
        return self.db.scalar(stmt)

    def exists(self, **filters: Any) -> bool:
        return self.first(**filters) is not None

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)

    def refresh(self, obj: ModelType) -> None:
        self.db.refresh(obj)

    def flush(self) -> None:
        self.db.flush()

    def execute(self, stmt: Select[Any]):
        return self.db.execute(stmt)
    
    def update(
        self,
        obj: ModelType,
        data: dict[str, Any],
    ) -> ModelType:
        for field, value in data.items():
            setattr(obj, field, value)
        return obj