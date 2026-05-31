from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, index=True, primary_key=True)
    username = Column(String)
    hashed_pass = Column(String, nullable=False)
    uuid = Column(String, nullable=False, unique=True)

    items = relationship("Items", backref="user")
