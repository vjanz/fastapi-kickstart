import uuid

import inflection
from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker
from sqlalchemy.sql import func

from src.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class DatabaseModel(Base):
    __abstract__ = True

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return inflection.pluralize(inflection.underscore(cls.__name__))

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
