from collections.abc import Generator

from sqlalchemy.orm import Session

from src.core.db import SessionLocal


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
