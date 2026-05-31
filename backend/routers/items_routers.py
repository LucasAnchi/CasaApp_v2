from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from services.item_service import create_item, get_items, update_item, delete_item, deactivate_item
from services.user_service import get_current_user
from models.schemas import ItemAdd, ItemUpdate, ItemResponse
from models.userModels import Users

router = APIRouter(prefix="/items", tags=["Items"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[Users, Depends(get_current_user)]


@router.get("/", response_model=list[ItemResponse])
async def list_items(db: db_dependency, current_user: current_user_dependency):
    return get_items(db, current_user.user_id)


@router.post("/", status_code=201)
async def add_item(item: ItemAdd, db: db_dependency, current_user: current_user_dependency):
    return create_item(db, item, current_user.user_id)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item_route(
    item_id: int,
    new_item: ItemUpdate,
    db: db_dependency,
    current_user: current_user_dependency,
):
    return await update_item(db, current_user.user_id, item_id, new_item)


@router.patch("/{item_id}/deactivate")
async def deactivate_item_route(
    item_id: int,
    db: db_dependency,
    current_user: current_user_dependency,
):
    return await deactivate_item(db, current_user.user_id, item_id)


@router.delete("/{item_id}")
async def delete_item_route(
    item_id: int,
    db: db_dependency,
    current_user: current_user_dependency,
):
    return await delete_item(db, current_user.user_id, item_id)
