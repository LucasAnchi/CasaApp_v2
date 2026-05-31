"""

ITEMS:

-> ID
-> OWNER_ID

-> Nome
-> Qntd
-> Marca
-> Preco
-> Categoria

-> Total_Add
-> Data

-> Ativo

"""

from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    DECIMAL,
    ForeignKey,
)


class Items(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    nome = Column(String(30), nullable=False)
    quantidade = Column(Float, default=0)
    preco = Column(DECIMAL(10, 0), default=0)

    marca = Column(String(30))
    categoria = Column(String(20))

    total_add = Column(Integer)
    add_data = Column(Date)

    ativo = Column(Boolean, nullable=False, default=False)
