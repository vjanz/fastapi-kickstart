from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.schemas.items import ItemCreate, ItemResponse
from src.services.item_service import create_item, get_item, get_items

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> Any:
    """
    Retrieve a list of items with optional pagination.

    This endpoint fetches items from the database, allowing for pagination
    using the `skip` and `limit` parameters. It returns a list of items
    matching the specified pagination criteria.

    Args:
        skip (int): The number of items to skip (default is 0).
        limit (int): The maximum number of items to return (default is 10).
        db (Session): The database session dependency.

    Returns:
        list[ItemResponse]: A list of items that match the pagination criteria.
    """
    items = get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Retrieve a single item by its ID.

    This endpoint fetches an item from the database based on the provided
    item ID. If the item is not found, a 404 error is raised.

    Args:
        item_id (int): The ID of the item to retrieve.
        db (Session): The database session dependency.

    Returns:
        ItemResponse: The item that matches the provided ID.

    Raises:
        HTTPException: 404 Not Found if the item does not exist.
    """
    item = get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)) -> Any:
    """
    Create a new item in the database.

    This endpoint creates a new item based on the provided item data. It
    returns the created item with a 201 Created status.

    Args:
        item (ItemCreate): The data for the new item.
        db (Session): The database session dependency.

    Returns:
        ItemResponse: The created item.
    """
    return create_item(db=db, item=item)
