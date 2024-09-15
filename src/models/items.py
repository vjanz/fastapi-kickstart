from sqlalchemy import Column, Integer, String

from src.core.db import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
