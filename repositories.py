''''
Camada única de isolamento das especificidades de acesso a base de dados.  
Código para operações de leitura e escrita no db.
'''

from sqlalchemy.orm import Session
from models import Product

# Lista todos os produtos
class ProductsRepository:
    @staticmethod
    def find_all(db: Session) -> list[Product]:
        return db.query(Product).all()

# Cadastro de novos e edição
    @staticmethod
    def save(db: Session, Product: Product) -> Product:
        if Product.id:
            db.merge(Product)
        else:
            db.add(Product)
        db.commit()
        return Product

# Busca Product por id no db
    @staticmethod
    def find_by_id(db: Session, id: int) -> Product:
        return db.query(Product).filter(Product.id == id).first()

# Consulta se existe
    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Product).filter(Product.id == id).first() is not None

# Exlui por id
    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        Product = db.query(Product).filter(Product.id == id).first()
        if Product is not None:
            db.delete(Product)
            db.commit()
