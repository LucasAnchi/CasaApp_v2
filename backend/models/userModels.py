from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, index=True, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    hashed_pass = Column(String(255), nullable=False)
    uuid = Column(String(36), nullable=False, unique=True)

    items = relationship("Items", backref="user")
