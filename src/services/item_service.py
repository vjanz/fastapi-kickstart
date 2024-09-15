from sqlalchemy.orm import Session

from src.models.items import Item
from src.schemas.items import ItemCreate


def get_item(db: Session, item_id: int) -> Item | None:
    """
    Retrieve an item from the database by its ID.

    Args:
        db (Session): The SQLAlchemy session object.
        item_id (int): The ID of the item to retrieve.

    Returns:
        Item | None: The item object if found, otherwise None.
    """
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10) -> list[Item]:
    """
    Retrieve a list of items from the database with optional pagination.

    Args:
        db (Session): The SQLAlchemy session object.
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to retrieve. Defaults to 10.

    Returns:
        list[Item]: A list of item objects.
    """
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate) -> Item:
    """
    Create a new item in the database.

    Args:
        db (Session): The SQLAlchemy session object.
        item (ItemCreate): The item data to create.

    Returns:
        Item: The created item object.
    """
    item_obj = Item(name=item.name)
    db.add(item_obj)
    db.commit()
    db.refresh(item_obj)
    return item_obj
