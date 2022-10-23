from email.mime import message
from fastapi import Body, FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Union

class Product(BaseModel):
    name: str = ""
    price: float = Field(default=10.0, gt=0, description="The price must be greater than zero")
    quantity: int = Field(default=1, ge=0, description="The quantity must be greater than or equal to zero")
    description: Union[str, None] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "price": 35.4,
                "quantity": 1,
                "description":"A very nice Product",
            }
        }

# Instance Created
app = FastAPI()

# Dabase
# Dictionary where keys are IDs and values are products (dicts)
product_1 = {"name" : "PS5", "price" : 5250, "description" : "White gaming console", "quantity" : 20}
product_2 = {"name" : "XBOX Series X", "price" : 4699.99, "description" : "Black gaming console", "quantity" : 15}
product_3 = {"name" : "HDMI1 Cable", "price" : 79.99, "description" : "Accessory", "quantity" : 50}
products_inventory = {0:product_1, 1:product_2, 2:product_3}

# Home
@app.get("/")
async def root():
    return {"Home Page"}

def product_in_inventory(product_id):
    if product_id not in products_inventory.keys():
        raise HTTPException(status_code = 404, detail = "Product not found in inventory!")

# Create Product [POST]
@app.post("/inventory/create", response_model=Product)
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
@app.get("/inventory/check", summary="Shows all the products available in the inventory")
async def check_inventory():
    return products_inventory

# Check by id
@app.get("/inventory/check/{id_product}", summary="Shows the product with the specified id")
async def check_inventory_product(id_product: int):
    product_in_inventory(id_product)
    return products_inventory[id_product]

# Update product details [PUT]
@app.put("/inventory/update/{id_product}", response_model=Product)
async def update_product(
    id_product: int,
    product: Product = Body(
        example = {
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8
        }
    )
):
    product_in_inventory(id_product)
    update_product_encoded = jsonable_encoder(product)
    products_inventory[id_product] = update_product_encoded
    return update_product_encoded

# Change products quantity [PATCH]
@app.patch("/inventory/edit/{id_product}", response_model=Product)
async def edit_product(
    id_product: int,
    product: Product = Body(
        example = {
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8
        }
    )
):
    product_in_inventory(id_product)
    stored_product_data = products_inventory[id_product]
    stored_product_model = Product(**stored_product_data)
    update_data = product.dict(exclude_unset=True)
    updated_product = stored_product_model.copy(update=update_data)
    products_inventory[id_product] = jsonable_encoder(updated_product)
    return updated_product

# Remove product from inventory [DELETE]
@app.delete("/inventory/remove/{id_product}", response_model=dict)
async def remove_product(id_product: int):
    product_in_inventory(id_product)
    products_inventory.pop(id_product)
    return products_inventory