from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    This class serves as the base class for all SQLAlchemy models in the application,
    providing the common metadata and configurations needed for ORM mapping.
    """

    ...
