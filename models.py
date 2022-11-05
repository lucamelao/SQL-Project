'''
SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
'''

# Classes do SQLAlchemy necessárias para a declaração do model
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(100), nullable=False, index=True)
    price: float = Column(Float, nullable=False)
    description: str = Column(String(255), nullable=False, index=True)

    inventory = relationship("Inventory", back_populates="products")
    movement = relationship("Movement", back_populates="products")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True, index=True)
    quantity: int = Column(Integer, nullable=False)

    products = relationship("Product", back_populates="inventory")

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True, index=True)
    quantity: int = Column(Integer, nullable=False)

    products = relationship("Product", back_populates="movement")