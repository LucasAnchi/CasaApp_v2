from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from services.lista_service import getLista, addItemLista, popularLista, updateItemLista, deleteItemLista, limparLista
from services.user_service import get_current_user
from models.schemas import ItemListaAdd, ItemListaUpdate, ItemListaResponse
from models.userModels import Users

router = APIRouter(prefix="/lista", tags=["ListaCompras"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[Users, Depends(get_current_user)]


@router.get("/", response_model=list[ItemListaResponse])
async def get_lista(db: db_dependency, current_user: current_user_dependency):
    return getLista(db, current_user.user_id)


@router.post("/", response_model=ItemListaResponse, status_code=201)
async def add_item(item: ItemListaAdd, db: db_dependency, current_user: current_user_dependency):
    return addItemLista(db, current_user.user_id, item)


@router.post("/popular", response_model=list[ItemListaResponse])
async def popular_lista(db: db_dependency, current_user: current_user_dependency):
    return popularLista(db, current_user.user_id)


@router.put("/{lista_id}", response_model=ItemListaResponse)
async def update_item(lista_id: int, new_item: ItemListaUpdate, db: db_dependency, current_user: current_user_dependency):
    return updateItemLista(db, current_user.user_id, lista_id, new_item)


@router.delete("/limpar")
async def limpar_lista(db: db_dependency, current_user: current_user_dependency):
    return limparLista(db, current_user.user_id)


@router.delete("/{lista_id}")
async def delete_item(lista_id: int, db: db_dependency, current_user: current_user_dependency):
    return deleteItemLista(db, current_user.user_id, lista_id)
