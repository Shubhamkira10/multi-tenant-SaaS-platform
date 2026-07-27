from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModel


class PlatformAdmin(BaseModel):
    __tablename__ = "platform_admins"

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="PLATFORM_OWNER",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )