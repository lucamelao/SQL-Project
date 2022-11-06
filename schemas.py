from typing import Union
from pydantic import BaseModel, Field

''''
Classes que representam os dados que serão recebidos e retornados no corpo de uma requisição ou resposta HTTP.
'''

class ProductBase(BaseModel):
    id: Union[int, None] = Field(default=1, gt=0, title="Product ID", description="The ID of the product.")
    name: str = Field(default="Product", title="Product name", description="The product must have a name.", max_length=300, example="Webcam")
    price: float = Field(default=0.0, gt=0, title="Product price", description="The price must be greater than zero.", example=4.39)
    description: Union[str, None] = Field(default=None, title="Product description", description="Any description concerning the product, optional.")
    
    class Config:
        # static method
        orm_mode = True

class ProductRequest(ProductBase):
    ...

class ProductResponse(ProductBase):
    class Config:
        # static method
        orm_mode = True

class InventoryBase(BaseModel):
    id: Union[int, None] = Field(default=1, gt=0, title="Product ID", description="The ID of the product in inventory.")
    quantity: int = Field(default=0, gt=0, title="Product quantity", description="The quantity of the product in the inventory.", example=20)
    
    class Config:
        # static method
        orm_mode = True

class InventoryRequest(InventoryBase):
    ...

class InventoryResponse(InventoryBase):
    class Config:
        # static method
        orm_mode = True

class MovementBase(BaseModel):
    id: int = Field(default=None, gt=0, title="Movement ID", description="The ID of the product movement.")
    quantity_change: int = Field(default=0, title="Movement quantity", description="The quantity of the product being moved.", example=20)
    id_product: int = Field(default=1, gt=0, title="Product ID", description="The ID of the product being moved.")

    class Config:
        # static method
        orm_mode = True

class MovementRequest(MovementBase):
    ...

class MovementResponse(MovementBase):
    class Config:
        # static method
        orm_mode = True
