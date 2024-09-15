from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
