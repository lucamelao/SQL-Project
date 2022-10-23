from email.mime import message
from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Union

class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="The price must be greater than zero")
    quantity: int = Field(ge=0, description="The quantity must be greater than or equal to zero")
    description: Union[str, None] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "price": 35.4,
                "quantity": 1,
                "description":"A very nice Item",
            }
        }

# Instance Created
app = FastAPI()

# Dabase
# Dictionary where keys are IDs and values are products (dicts)
product_1 = {"name" : "PS5", "price" : 5250, "description" : "White gaming console", "quantity" : 20}
product_2 = {"name" : "XBOX Series X", "price" : 4699.99, "description" : "Black gaming console", "quantity" : 15}
product_3 = {"name" : "HDMI1 Cable", "price" : 79.99, "description" : "Acessory", "quantity" : 50}
products_inventory = {0:product_1, 1:product_2, 2:product_3}

# Home
@app.get("/")
async def root():
    return {"Home Page"}

def product_in_inventory(product_id):
    if product_id not in products_inventory.keys():
        raise HTTPException(status_code = 404, detail = "Product not found in inventory!")

# Create Product [POST]
@app.post("/Inventory/Create", response_model=Product)
async def create_product(
    product: Product = Body(
        example = {
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8,
            "description":"A very beautiful keyboard"
        }
    )
):
    products_inventory[len(products_inventory)] = product
    return product

# Check inventory [GET]
@app.get("/Inventory/Check", summary="Shows all the products available in the inventory")
async def check_inventory():
    return products_inventory

# Check by id
@app.get("/Inventory/Check/{id_product}", summary="Shows the product with the specified id")
async def check_inventory_product(id_product:int):
    product_in_inventory(id_product)
    return products_inventory[id_product]

# Edit product details [PUT]

# Change products quantity [PATCH]

# Remove product from inventory [DELETE]