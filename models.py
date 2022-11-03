'''
SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
'''

# Classes do SQLAlchemy necessárias para a declaração do model
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False, index=True)
    price: float = Column(Float, nullable=False)
    quantity: int = Column(Integer, nullable=False)
    description: str = Column(String(255), nullable=False, index=True)