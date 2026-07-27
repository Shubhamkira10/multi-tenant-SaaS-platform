from __future__ import annotations

from math import ceil
from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class PageMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool = True
    message: str = "Success"
    data: Sequence[T]
    meta: PageMeta


def paginate(
    items: Sequence[T],
    total: int,
    page: int,
    per_page: int,
) -> PaginatedResponse[T]:
    return PaginatedResponse(
        data=items,
        meta=PageMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=ceil(total / per_page) if per_page else 1,
        ),
    )