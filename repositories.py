''''
Camada única de isolamento das especificidades de acesso a base de dados.  
Código para operações de leitura e escrita no db.
'''

from sqlalchemy.orm import Session
from models import Product, Inventory, Movement

# Lista todos os produtos
class ProductsRepository:
    @staticmethod
    def find_all(db: Session) -> list[Product]:
        return db.query(Product).all()

# Cadastro de novos
    @staticmethod
    def add(db: Session, product: Product) -> Product:
        try:
            db.add(product)
            db.commit()
        except:
            ...
        return product

# Edição
    @staticmethod
    def update(db: Session, product: Product) -> Product:
        try:
            db.merge(product)
            db.commit()
        except:
            ...
        return product

# Busca Product por id no db
    @staticmethod
    def find_by_id(db: Session, id: int) -> Product:
        return db.query(Product).filter(Product.id == id).first()

# Consulta se existe
    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Product).filter(Product.id == id).first() is not None

# Exclui por id
    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        product = db.query(product).filter(product.id == id).first()
        if product is not None:
            db.delete(product)
            db.commit()
            

# Lista todos os produtos
class InventoryRepository:
    @staticmethod
    def find_all(db: Session) -> list[Inventory]:
        return db.query(Inventory).all()

# Cadastro de novos
    @staticmethod
    def add(db: Session, inventory: Inventory) -> Inventory:
        try:
            db.add(inventory)
            db.commit()
        except:
            ...
        return inventory

# Edição
    @staticmethod
    def update(db: Session, inventory: Inventory) -> Inventory:
        try:
            db.merge(inventory)
            db.commit()
        except:
            ...
        return inventory

# Busca Inventory por id no db
    @staticmethod
    def find_by_id(db: Session, id: int) -> Inventory:
        return db.query(Inventory).filter(Inventory.id == id).first()

# Consulta se existe
    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Inventory).filter(Inventory.id == id).first() is not None

# Exclui por id
    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        inventory = db.query(inventory).filter(inventory.id == id).first()
        if inventory is not None:
            db.delete(inventory)
            db.commit()
            

# Lista todos os produtos
class MovementRepository:
    @staticmethod
    def find_all(db: Session) -> list[Movement]:
        return db.query(Movement).all()

# Cadastro de novos
    @staticmethod
    def add(db: Session, movement: Movement) -> Movement:
        try:
            db.add(movement)
            db.commit()
        except:
            ...
        return movement

# Busca Movement por id no db
    @staticmethod
    def find_by_id(db: Session, id: int) -> Movement:
        return db.query(Movement).filter(Movement.id == id).first()

# Consulta se existe
    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Movement).filter(Movement.id == id).first() is not None
