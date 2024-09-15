from sqlalchemy.orm import Session

from src.models import Item
from src.schemas.items import ItemCreate
from src.services.item_service import create_item, get_item


def test_create_item(db_session: Session) -> None:
    """
    Test the creation of an item.

    Args:
        db_session (Session): The SQLAlchemy session to use for database operations.
    """
    item_data = ItemCreate(name="Test Item")
    created_item = create_item(db=db_session, item=item_data)

    assert created_item.id is not None
    assert created_item.name == "Test Item"

    item_in_db = (
        db_session.query(created_item.__class__).filter_by(id=created_item.id).first()
    )
    assert item_in_db is not None
    assert item_in_db.name == "Test Item"
    assert item_in_db.id is not None


def test_get_item(db_session: Session, item: Item) -> None:
    """
    Test retrieving an item by its ID.

    Args:
        db_session (Session): The SQLAlchemy session to use for database operations.
        item (Item): The item to be retrieved from the database.
    """
    fetched_item = get_item(db=db_session, item_id=item.id)  # type: ignore

    assert fetched_item is not None
    assert fetched_item.id == item.id
    assert fetched_item.name == item.name


def test_get_item_not_found(db_session: Session) -> None:
    """
    Test retrieving an item that does not exist.

    Args:
        db_session (Session): The SQLAlchemy session to use for database operations.
    """
    fetched_item = get_item(db=db_session, item_id=9999)

    assert fetched_item is None
