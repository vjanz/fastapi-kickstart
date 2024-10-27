from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.core.db import DatabaseModel

ModelType = TypeVar("ModelType", bound=DatabaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get(self, id: UUID) -> ModelType | None:
        try:
            return self.db.query(self.model).filter(self.model.id == id).one()
        except NoResultFound:
            return None

    def get_all(self) -> list[ModelType]:
        return self.db.query(self.model).all()

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        self.db.commit()
        return obj

    def delete(self, id: UUID) -> None:
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
