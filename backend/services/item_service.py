from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.schemas import ItemAdd, ItemUpdate, ItemResponse
from models.userModels import Users
from models.itemModels import Items
import datetime


def get_items(db: Session, user_id: int) -> list[ItemResponse]:
    items = db.query(Items).filter(Items.owner_id == user_id).all()
    return [ItemResponse.model_validate(item) for item in items]


def create_item(db: Session, create_item_request: ItemAdd, user_id: int):
    create_item_model = Items(
        owner_id=user_id,
        nome=create_item_request.nome,
        quantidade=create_item_request.quantidade,
        preco=create_item_request.preco,
        marca=create_item_request.marca,
        categoria=create_item_request.categoria,
        total_add=create_item_request.quantidade,
        add_data=datetime.date.today(),
        ativo=True,
    )

    db.add(create_item_model)
    db.commit()
    db.refresh(create_item_model)
    return {"message": "Item criado com sucesso"}


async def update_item(db: Session, user_id: int, item_id: int, new_item: ItemUpdate):
    current_user = db.query(Users).filter(Users.user_id == user_id).first()
    if not current_user:
        raise HTTPException(404, "Usuário não encontrado")

    item = db.query(Items).filter(Items.item_id == item_id).first()
    if not item:
        raise HTTPException(404, "Item não encontrado")

    if item.owner_id != current_user.user_id:
        raise HTTPException(403, "Você não pode modificar esse item")

    if new_item.nome is not None:
        item.nome = new_item.nome
    if new_item.quantidade is not None:
        item.total_add = max(item.quantidade or 0, new_item.quantidade)
        item.quantidade = new_item.quantidade
    if new_item.preco is not None:
        item.preco = new_item.preco
    if new_item.marca is not None:
        item.marca = new_item.marca
    if new_item.categoria is not None:
        item.categoria = new_item.categoria

    db.commit()
    db.refresh(item)

    return ItemResponse.model_validate(item)


async def delete_item(db: Session, user_id: int, item_id: int):
    current_user = db.query(Users).filter(Users.user_id == user_id).first()
    if not current_user:
        raise HTTPException(404, "Usuário não encontrado")

    item = db.query(Items).filter(Items.item_id == item_id).first()
    if not item:
        raise HTTPException(404, "Item não encontrado")

    if item.owner_id != current_user.user_id:
        raise HTTPException(403, "Você não pode modificar esse item")

    db.delete(item)
    db.commit()

    return {"message": "Item deletado"}


async def deactivate_item(db: Session, user_id: int, item_id: int):
    current_user = db.query(Users).filter(Users.user_id == user_id).first()
    if not current_user:
        raise HTTPException(404, "Usuário não encontrado")

    item = db.query(Items).filter(Items.item_id == item_id).first()
    if not item:
        raise HTTPException(404, "Item não encontrado")

    if item.owner_id != current_user.user_id:
        raise HTTPException(403, "Você não pode modificar esse item")

    item.ativo = False
    db.commit()
    db.refresh(item)

    return {"message": "Item desativado"}
