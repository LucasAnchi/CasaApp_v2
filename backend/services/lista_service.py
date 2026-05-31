import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.schemas import ItemListaAdd, ItemListaUpdate, ItemListaResponse
from models.itemModels import Items
from models.listaModels import ListaCompras


def getOptimalQuantidade(item: Items) -> float:
    if item.add_data is None or item.total_add is None:
        return 0

    today = datetime.date.today()
    months = (today.year - item.add_data.year) * 12 + (today.month - item.add_data.month)

    if months == 0:
        return float(item.total_add)

    return item.total_add / months


def getLista(db: Session, user_id: int) -> list[ItemListaResponse]:
    items = db.query(ListaCompras).filter(ListaCompras.owner_id == user_id).all()
    return [ItemListaResponse.model_validate(item) for item in items]


def addItemLista(db: Session, user_id: int, item: ItemListaAdd) -> ItemListaResponse:
    novo_item = ListaCompras(
        owner_id=user_id,
        nome=item.nome,
        quantidade=item.quantidade,
        preco=item.preco,
        marca=item.marca,
    )
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return ItemListaResponse.model_validate(novo_item)


def popularLista(db: Session, user_id: int) -> list[ItemListaResponse]:
    items_estoque = db.query(Items).filter(
        Items.owner_id == user_id,
        Items.ativo == True,
    ).all()

    for item in items_estoque:
        ja_existe = db.query(ListaCompras).filter(
            ListaCompras.owner_id == user_id,
            ListaCompras.nome == item.nome,
        ).first()

        if not ja_existe:
            quantidade = getOptimalQuantidade(item)
            db.add(ListaCompras(
                owner_id=user_id,
                nome=item.nome,
                quantidade=quantidade,
                preco=item.preco,
                marca=item.marca,
            ))

    db.commit()
    return getLista(db, user_id)


def updateItemLista(db: Session, user_id: int, lista_id: int, new_item: ItemListaUpdate) -> ItemListaResponse:
    item = db.query(ListaCompras).filter(
        ListaCompras.lista_id == lista_id,
        ListaCompras.owner_id == user_id,
    ).first()

    if not item:
        raise HTTPException(404, "Item não encontrado na lista")

    if new_item.nome is not None:
        item.nome = new_item.nome
    if new_item.quantidade is not None:
        item.quantidade = new_item.quantidade
    if new_item.preco is not None:
        item.preco = new_item.preco
    if new_item.marca is not None:
        item.marca = new_item.marca

    db.commit()
    db.refresh(item)
    return ItemListaResponse.model_validate(item)


def deleteItemLista(db: Session, user_id: int, lista_id: int) -> dict:
    item = db.query(ListaCompras).filter(
        ListaCompras.lista_id == lista_id,
        ListaCompras.owner_id == user_id,
    ).first()

    if not item:
        raise HTTPException(404, "Item não encontrado na lista")

    db.delete(item)
    db.commit()
    return {"message": "Item removido da lista"}


def limparLista(db: Session, user_id: int) -> dict:
    db.query(ListaCompras).filter(ListaCompras.owner_id == user_id).delete()
    db.commit()
    return {"message": "Lista limpa"}
