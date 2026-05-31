from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import String


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_pass: Mapped[str] = mapped_column(String(255), nullable=False)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)

    items: Mapped[List["Items"]] = relationship("Items", backref="user")
