from collections.abc import Generator

import jwt
from fastapi import Depends, HTTPException
from passlib.exc import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from src.core.config import settings
from src.core.db import SessionLocal
from src.core.enums import UserType
from src.core.security import oauth2_scheme
from src.models import User
from src.repositories.item import ItemRepository
from src.repositories.user import UserRepository
from src.services.auth import AuthService
from src.services.item import ItemService
from src.services.user import UserService


def get_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session for database operations.

    This generator function yields a SQLAlchemy session object, ensuring
    that the session is properly closed after use. It is used to manage
    database connections and ensure they are cleanly closed to prevent
    resource leaks.

    Yields:
        Session: A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    item_repository = ItemRepository(db)
    return ItemService(item_repository)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
