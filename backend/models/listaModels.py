import decimal
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import String, Float, DECIMAL, ForeignKey


class ListaCompras(Base):
    __tablename__ = "lista_compras"

    lista_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    quantidade: Mapped[Optional[float]] = mapped_column(Float)
    preco: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    marca: Mapped[Optional[str]] = mapped_column(String(30))
