from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import (
    get_current_active_superuser,
    get_current_user,
    get_item_service,
    get_user_service,
)
from src.models import Item
from src.models.users import User
from src.schemas.auth import UserRead
from src.schemas.items import ItemCreate, ItemRead
from src.services.item import ItemService
from src.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/users", response_model=list[UserRead])
def users(
    user_service: UserService = Depends(get_user_service),
    _: None = Depends(get_current_active_superuser),
) -> list[User]:
    return user_service.get_all()


@router.post("/users/{user_id}/items", response_model=ItemRead)
def create_user_item(
    user_id: UUID,
    item: ItemCreate,
    item_service: ItemService = Depends(get_item_service),
    current_user: User = Depends(get_current_user),
) -> Item:
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    return item_service.create_item(user_id=user_id, item=item)


@router.get("/users/{user_id}/items", response_model=list[ItemRead])
def get_user_items(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
) -> list[Item]:
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user.items
