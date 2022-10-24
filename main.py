from email.mime import message
from fastapi import Body, FastAPI, status, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Union

example = {
    "name" : "Keyboard",
    "price": 1250.2,
    "quantity": 8,
    "description":"A very beautiful keyboard",
}

class Product(BaseModel):
    name: str = ""
    price: float = Field(default=10.0, gt=0, description="The price must be greater than zero")
    quantity: int = Field(default=1, ge=0, description="The quantity must be greater than or equal to zero")
    description: Union[str, None] = Field(default=None, description="Any description concerning the product, optional")
    
    class Config:
        schema_extra = {"example": example}

# Instance Created
app = FastAPI()

# Dabase
# Dictionary where keys are IDs and values are products (dicts)
product_1 = {
    "name" : "PS5",
    "price" : 5250,
    "quantity" : 20,
    "description" : "White gaming console",
}
product_2 = {
    "name" : "XBOX Series X",
    "price" : 4699.99,
    "quantity" : 15,
    "description" : "Black gaming console",
}
product_3 = {
    "name" : "HDMI1 Cable",
    "price" : 79.99,
    "quantity" : 50,
    "description" : "Accessory",
}
products_inventory = {0:product_1, 1:product_2, 2:product_3}

     
# Home
@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    """
        Home Page
    """
    return '''
     <html>
        <head>
        <title> Home Page </title>
        </head>
        <body>
            <h1> Home Page </h1>
            <h2> Access the following routes for each request: </h2>
            <li> http://127.0.0.1:8000/inventory/create </li>
            <li>http://127.0.0.1:8000/inventory/check</li>
            <li>http://127.0.0.1:8000/inventory/check/{id_product}</li>
            <li>http://127.0.0.1:8000/inventory/update/{id_product}</li>
            <li>http://127.0.0.1:8000/inventory/edit/{id_product}</li>
            <li>http://127.0.0.1:8000/inventory/remove/{id_product}</li>
            <h3>By Luca and Mat</h3>
        </body>
    </html>
    '''

def product_in_inventory(product_id):
    if product_id not in products_inventory.keys():
        raise HTTPException(status_code = 404, detail = "Product not found in inventory!")

# Create Product [POST]
@app.post("/inventory/create/{id_product}", response_model = Product, summary= "Create a product", status_code=201, tags=["Create"])
async def create_product(
    id_product: int = Path(title="The ID of the product you want to create", ge=0),
    product: Product = Body(example = example),
):
    """

        Create a product with all the information, if the ID doesn't exist:
        - **name**: product name
        - **price**: product price
        - **quantity**: quantity in inventory
        - **description** *[optional]*: product description

        Return example:

        {
        
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8,
            "description":"A very beautiful keyboard"
        
        }

    """
    if id_product in products_inventory.keys():
        raise HTTPException(status_code=409, detail="ID already exists! Give a different ID number.")
    products_inventory[id_product] = product
    return product

# Check inventory [GET]
@app.get("/inventory/check", summary= "Shows all the products available in the inventory", status_code=200, tags=["Consult"])
async def check_inventory():
    """

        Check the products in inventory, returns a dictionary of the products' IDs and the corresponding product. Each product has the following attributes:
        - **name**: product name
        - **price**: product price
        - **quantity**: quantity in inventory
        - **description** *[optional]*: product description

        Return example:

        {

            "0": {
                "name": "PS5",
                "price": 5250,
                "quantity": 20,
                "description": "White gaming console"
            },
            "1": {
                "name": "XBOX Series X",
                "price": 4699.99,
                "quantity": 15,
                "description": "Black gaming console"
            },
            "2": {
                "name": "HDMI1 Cable",
                "price": 79.99,
                "quantity": 50,
                "description": "Accessory"
            }
        }

    """
    return products_inventory

# Check by id
@app.get("/inventory/check/{id_product}", summary="Shows the product from the inventory with the specified id", status_code=200, tags=["Consult"])
async def check_inventory_product(id_product: int = Path(title="The ID of the product you want to check on inventory", ge=0)):
    """

        Check a product in inventory by its ID if it exists, returns the following product attributes:
        - **name**: product name
        - **price**: product price
        - **quantity**: quantity in inventory
        - **description** *[optional]*: product description

        Return example:

        {
        
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8,
            "description":"A very beautiful keyboard"
        
        }

    """
    product_in_inventory(id_product)
    return products_inventory[id_product]

# Update product details [PUT]
@app.put("/inventory/update/{id_product}", response_model=Product, status_code=200, tags=["Edit"])
async def update_product(
    id_product: int = Path(title="The ID of the product you want to edit", ge=0),
    product: Product = Body(example = example),
):
    """

        Update a product in inventory by its ID if it exists, returns the following updated product attributes:
        - **name**: product name
        - **price**: product price
        - **quantity**: quantity in inventory
        - **description** *[optional]*: product description
        All the non-optional attributes must be filled out, otherwise default values replace the old values where new value is missing.

        Return example:

        {
        
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8,
            "description":"A very beautiful keyboard"
        
        }

    """
    product_in_inventory(id_product)
    update_product_encoded = jsonable_encoder(product)
    products_inventory[id_product] = update_product_encoded
    return update_product_encoded

# Change products quantity [PATCH]
@app.patch("/inventory/edit/{id_product}", response_model=Product, status_code=200, tags=["Edit"])
async def edit_product(
    id_product: int = Path(title="The ID of the product you want to edit", ge=0),
    product: Product = Body(example = example),
):
    """

        Patch a product in inventory by its ID if it exists, returns the following product attributes:
        - **name**: product name
        - **price**: product price
        - **quantity**: quantity in inventory
        - **description** *[optional]*: product description
        Patch is a "partial update", so only attributes with desired modifications need to be filled out.

        Return example:

        {
        
            "name" : "Keyboard",
            "price": 1250.2,
            "quantity": 8,
            "description":"A very beautiful keyboard"
        
        }

    """
    product_in_inventory(id_product)
    stored_product_data = products_inventory[id_product]
    stored_product_model = Product(**stored_product_data)
    update_data = product.dict(exclude_unset=True)
    updated_product = stored_product_model.copy(update=update_data)
    products_inventory[id_product] = jsonable_encoder(updated_product)
    return updated_product

# Remove product from inventory [DELETE]
@app.delete("/inventory/remove/{id_product}", response_model=dict, status_code=200, tags=["Remove"])
async def remove_product(id_product: int = Path(title="The ID of the product you want to delete", ge=0)):
    """

        Remove a product in inventory by ID, returns a dictionary of the products' IDs and the corresponding product. Each product has the following attributes:
        - **name**: product name
        - **price**: product price
        - **quantity**: quantity in inventory
        - **description** *[optional]*: product description

        Return example:

        {

            "0": {
                "name": "PS5",
                "price": 5250,
                "quantity": 20,
                "description": "White gaming console"
            },
            "1": {
                "name": "XBOX Series X",
                "price": 4699.99,
                "quantity": 15,
                "description": "Black gaming console"
            },
            "2": {
                "name": "HDMI1 Cable",
                "price": 79.99,
                "quantity": 50,
                "description": "Accessory"
            }
        }

    """
    product_in_inventory(id_product)
    del products_inventory[id_product]
    return products_inventory