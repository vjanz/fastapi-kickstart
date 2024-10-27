from typing import Generic, TypeVar
from uuid import UUID

from src.core.db import DatabaseModel
from src.repositories.base import BaseRepository

ServiceModelType = TypeVar("ServiceModelType", bound=DatabaseModel)


class BaseService(Generic[ServiceModelType]):
    def __init__(self, repository: BaseRepository[ServiceModelType]):
        self.repository = repository

    def get(self, id: UUID) -> ServiceModelType:
        return self.repository.get(id)  # type: ignore

    def get_all(self) -> list[ServiceModelType]:
        return self.repository.get_all()

    def create(self, obj: ServiceModelType) -> ServiceModelType:
        return self.repository.create(obj)

    def update(self, obj: ServiceModelType) -> ServiceModelType:
        return self.repository.update(obj)

    def delete(self, id: UUID) -> bool:
        try:
            self.repository.delete(id)
            return True
        except Exception:
            return False
