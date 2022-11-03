from typing import Union
from pydantic import BaseModel

''''
Classes que representam os dados que serão recebidos e retornados no corpo de uma requisição ou resposta HTTP.
'''

class ProductBase(BaseModel):
    id: int
    name: str 
    price: float
    quantity: int 
    description: Union[str, None] = None
    
    class Config:
        # static method
        orm_mode = True

class ProductRequest(ProductBase):
    ...

class ProductResponse(ProductBase):
    id: int

    class Config:
        # static method
        orm_mode = True
