import uuid

from src.models import Item
from src.repositories.item import ItemRepository
from src.schemas.items import ItemCreate
from src.services.base import BaseService


class ItemService(BaseService[Item]):
    def __init__(self, item_repository: ItemRepository):
        super().__init__(item_repository)
        self.item_repository = item_repository

    def create_item(self, user_id: uuid.UUID, item: ItemCreate) -> Item:
        item_obj = Item(**item.dict(), user_id=user_id)
        return self.item_repository.create(item_obj)
