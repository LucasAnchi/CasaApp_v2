import datetime
import decimal
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import String, Float, Date, Boolean, DECIMAL, ForeignKey


class Items(Base):
    __tablename__ = "items"

    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    quantidade: Mapped[Optional[float]] = mapped_column(Float, default=0)
    preco: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), default=0)

    marca: Mapped[Optional[str]] = mapped_column(String(30))
    categoria: Mapped[Optional[str]] = mapped_column(String(20))

    total_add: Mapped[Optional[int]] = mapped_column()
    add_data: Mapped[Optional[datetime.date]] = mapped_column(Date)

    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
