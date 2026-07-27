from __future__ import annotations

from fastapi import HTTPException, status


class PlatformException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class BadRequestException(PlatformException):
    def __init__(self, detail: str = "Bad Request") -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail,
        )


class UnauthorizedException(PlatformException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail,
        )


class ForbiddenException(PlatformException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail,
        )


class NotFoundException(PlatformException):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            detail,
        )


class ConflictException(PlatformException):
    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(
            status.HTTP_409_CONFLICT,
            detail,
        )


class ValidationException(PlatformException):
    def __init__(self, detail: str = "Validation failed") -> None:
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail,
        )


class InternalServerException(PlatformException):
    def __init__(self, detail: str = "Internal Server Error") -> None:
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail,
        )