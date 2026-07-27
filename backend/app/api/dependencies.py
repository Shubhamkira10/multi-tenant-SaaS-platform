from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db

DBSession = Annotated[Session, Depends(get_db)]


class Pagination:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
    ) -> None:
        self.page = page
        self.per_page = per_page

        self.offset = (page - 1) * per_page
        self.limit = per_page


PaginationParams = Annotated[Pagination, Depends()]