from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: T | None = None

    @classmethod
    def ok(cls, data=None, message="Success"):
        return cls(
            success=True,
            message=message,
            data=data,
        )

    @classmethod
    def fail(cls, message="Error", data=None):
        return cls(
            success=False,
            message=message,
            data=data,
        )