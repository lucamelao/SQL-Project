from fastapi import Body, FastAPI, status, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from typing import Union

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

import models
from database import engine, Base, get_db
from repositories import ProductsRepository
from schemas import ProductBase, ProductRequest, ProductResponse


models.Base.metadata.create_all(bind=engine)

# Instance Created
app = FastAPI()


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

def product_in_inventory(db, id):
    if not ProductsRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Product not found in inventory!"
            )

# Create Product [POST]
@app.post("/inventory/create", response_model = ProductResponse, summary= "Create a product", status_code=201, tags=["Create"])
def create_product(request: ProductRequest, db: Session = Depends(get_db)):
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
    #if id_product in products_inventory.keys():
    #    raise HTTPException(status_code=409, detail="ID already exists! Give a different ID number.")
    
    product = ProductsRepository.save(db, Product(**request.dict()))
    return ProductResponse.from_orm(product)

# Check inventory [GET]
@app.get("/inventory/check", summary= "Shows all the products available in the inventory", status_code=200, tags=["Consult"], response_model=list[ProductResponse])
def check_inventory(db: Session = Depends(get_db)):
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
    products = ProductsRepository.find_all(db)
    return [ProductResponse.from_orm(product) for product in products]

# Check by id
@app.get("/inventory/check/{id_product}", summary="Shows the product from the inventory with the specified id", status_code=200, tags=["Consult"], response_model=ProductResponse)
def check_inventory_product(id: int, db: Session = Depends(get_db)):
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
    product_in_inventory(db, id)
    product = ProductsRepository.find_by_id(db, id)
    return ProductResponse.from_orm(product)

# Update product details [PUT]
@app.put("/inventory/update/{id_product}", response_model=ProductResponse, status_code=200, tags=["Edit"])
async def update_product(id: int, request: ProductRequest, db: Session = Depends(get_db)):
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
    product_in_inventory(db, id)
    product = ProductsRepository.save(db, Product(id=id, **request.dict()))
    return ProductResponse.from_orm(product)

# Change products quantity [PATCH]
@app.patch("/inventory/edit/{id_product}", response_model=ProductResponse, status_code=200, tags=["Edit"])
async def edit_product(id: int, request: ProductRequest, db: Session = Depends(get_db)):
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
    product_in_inventory(db, id)
    product = ProductsRepository.save(db, Product(id=id, **request.dict()))
    return ProductResponse.from_orm(product)

# Remove product from inventory [DELETE]
@app.delete("/inventory/remove/{id_product}", status_code=status.HTTP_204_NO_CONTENT, tags=["Remove"])
def remove_product(id: int, db: Session = Depends(get_db)):
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
    product_in_inventory(db, id)
    ProductsRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)