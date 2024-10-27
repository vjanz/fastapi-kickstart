import uuid

from src.schemas.base import BaseSchema


class ItemBase(BaseSchema):
    name: str


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: uuid.UUID
