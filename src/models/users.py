from typing import Any

from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import DatabaseModel
from src.core.enums import UserType


class User(DatabaseModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_type: Mapped[UserType] = mapped_column(
        SQLAlchemyEnum(UserType), nullable=False, default=UserType.USER
    )

    items: Mapped[list[Any]] = relationship(
        "Item", back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email}, user_type={self.user_type})>"

    def __str__(self) -> str:
        return f"{self.name} ({self.user_type})"
