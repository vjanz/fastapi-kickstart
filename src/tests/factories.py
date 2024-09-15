import uuid

import pytest
from sqlalchemy.orm import Session

from src.models import Item
from src.schemas.items import ItemCreate
from src.services.item_service import create_item


@pytest.fixture
def item(db_session: Session) -> Item:
    random_name = f"Test Item {uuid.uuid4().hex[:6]}"
    item_data = ItemCreate(name=random_name)
    return create_item(db=db_session, item=item_data)
