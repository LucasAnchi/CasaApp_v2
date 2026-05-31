import decimal
from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    username: str


class UserAdd(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class ItemBase(BaseModel):
    nome: str
    quantidade: Optional[float] = None
    preco: Optional[decimal.Decimal] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None


class ItemAdd(ItemBase):
    pass


class ItemUpdate(BaseModel):
    nome: Optional[str] = None
    quantidade: Optional[float] = None
    preco: Optional[decimal.Decimal] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None


class ItemResponse(BaseModel):
    item_id: int
    #    owner_id: int
    nome: str
    quantidade: Optional[float] = None
    preco: Optional[decimal.Decimal] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user_id: int
    username: str
    items: List[ItemResponse]

    class Config:
        from_attributes = True
        
        
class ItemLista(BaseModel):
    nome: str
    quantidade: Optional[float] = None
    preco: Optional[decimal.Decimal] = None
    marca: Optional[str] = None

    class Config:
        from_attributes = True


class ItemListaResponse(ItemLista):
    lista_id: int
    
    
class ItemListaAdd(ItemLista):
    pass

class ItemListaUpdate(BaseModel):
    nome: Optional[str] = None
    quantidade: Optional[float] = None
    preco: Optional[decimal.Decimal] = None
    marca: Optional[str] = None
    
    
class ListaCompras(BaseModel):
    items: List[ItemLista]
    