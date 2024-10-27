from sqlalchemy.orm import Session

from src.models import Item
from src.repositories.base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(db, Item)
