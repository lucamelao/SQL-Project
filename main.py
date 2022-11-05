from fastapi import Body, FastAPI, status, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from typing import Union

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models import Product, Inventory, Movement, Base
from database import engine, Base, get_db
from repositories import ProductsRepository, InventoryRepository, MovementRepository
from schemas import ProductRequest, ProductResponse, InventoryRequest, InventoryResponse, MovementRequest, MovementResponse


Base.metadata.create_all(bind=engine)

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

def product_exists(db, id):
    if not ProductsRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Product does not exists!"
            )

def product_in_inventory(db, id):
    if not InventoryRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Product not in inventory!"
            )

# ------------------------------------------------- PRODUCTS -------------------------------------------------

# Check products [GET]
@app.get("/product/check", summary= "Shows all the existing products", status_code=200, tags=["Product"], response_model=list[ProductResponse])
async def check_product(db: Session = Depends(get_db)):
    """

        Check the existing products, returns a list of the existing products. Each product has the following attributes:
        - **id**: product ID
        - **name**: product name
        - **price**: product price
        - **description** *[optional]*: product description

        Return example:

        [

            {
                "id": 1,
                "name": "PS5",
                "price": 5250,
                "description": "White gaming console"
            },
            {
                "id": 5,
                "name": "XBOX Series X",
                "price": 4699.99,
                "description": "Black gaming console"
            },
            {
                "id": 2,
                "name": "HDMI1 Cable",
                "price": 79.99,
                "description": "Accessory"
            }
        ]

    """
    products = ProductsRepository.find_all(db)
    return [ProductResponse.from_orm(product) for product in products]

# Check by id [GET]
@app.get("/product/check/{id_product}", summary="Shows the existing product with the specified id", status_code=200, tags=["Product"], response_model=ProductResponse)
async def check_product_by_id(id: int, db: Session = Depends(get_db)):
    """

        Check an existing product by its ID if it exists, returns the following product attributes:
        - **id**: product ID
        - **name**: product name
        - **price**: product price
        - **description** *[optional]*: product description

        Return example:

        {
        
            "id": 4,
            "name" : "Keyboard",
            "price": 1250.2,
            "description":"A very beautiful keyboard"
        
        }

    """
    product_exists(db, id)
    product = ProductsRepository.find_by_id(db, id)
    return ProductResponse.from_orm(product)

# Create Product [POST]
@app.post("/product/create", response_model = ProductResponse, summary= "Create a product", status_code=201, tags=["Product"])
async def create_product(request: ProductRequest, db: Session = Depends(get_db)):
    """

        Create a product with all the information, if the ID doesn't exist:
        - **name**: product name
        - **price**: product price
        - **description** *[optional]*: product description

        Return example:

        {
        
            "id": 4,
            "name" : "Keyboard",
            "price": 1250.2,
            "description":"A very beautiful keyboard"
        
        }

    """
    product = Product(**request.dict())
    if ProductsRepository.exists_by_id(db, product.id):
        raise HTTPException(
            status_code=409,
            detail="ID already exists! Give a different ID number."
        )
    product = ProductsRepository.add(db, product)
    return ProductResponse.from_orm(product)

# Update product details [PUT]
@app.put("/product/update/{id_product}", response_model=ProductResponse, status_code=200, tags=["Product"])
async def update_product(id: int, request: ProductRequest, db: Session = Depends(get_db)):
    """

        Update an existing product by its ID if it exists, returns the following updated product attributes:
        - **id**: product ID
        - **name**: product name
        - **price**: product price
        - **description** *[optional]*: product description
        All the non-optional attributes must be filled out, otherwise default values replace the old values where new value is missing.

        Return example:

        {
        
            "id": 4,
            "name" : "Keyboard",
            "price": 1250.2,
            "description":"A very beautiful keyboard"
        
        }

    """
    product_exists(db, id)
    product = ProductsRepository.add(db, Product(id=id, **request.dict()))
    return ProductResponse.from_orm(product)

# Edit products details [PATCH]
@app.patch("/product/edit/{id_product}", response_model=ProductResponse, status_code=200, tags=["Product"])
async def edit_product(id: int, request: ProductRequest, db: Session = Depends(get_db)):
    """

        Patch an existing product by its ID if it exists, returns the following product attributes:
        - **id**: product ID
        - **name**: product name
        - **price**: product price
        - **description** *[optional]*: product description
        Patch is a "partial update", so only attributes with desired modifications need to be filled out.

        Return example:

        {
        
            "id": 4,
            "name" : "Keyboard",
            "price": 1250.2,
            "description":"A very beautiful keyboard"
        
        }

    """
    product_exists(db, id)
    product = ProductsRepository.add(db, Product(id=id, **request.dict()))
    return ProductResponse.from_orm(product)

# Remove product from listing [DELETE]
@app.delete("/product/remove/{id_product}", status_code=status.HTTP_204_NO_CONTENT, tags=["Product"])
async def remove_product(id: int, db: Session = Depends(get_db)):
    """

        Remove an existing product by ID, no return.

    """
    product_exists(db, id)
    ProductsRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------- INVENTORY -------------------------------------------------

# Check inventory [GET]
@app.get("/inventory/check", summary= "Shows all the products available in the inventory", status_code=200, tags=["Inventory"], response_model=list[InventoryResponse])
async def check_inventory(db: Session = Depends(get_db)):
    """

        Check the products in inventory, returns a list of the products in inventory. Each inventory product has the following attributes:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        [

            {
                "id": 1,
                "quantity": 4
            },
            {
                "id": 5,
                "quantity": 6
            },
            {
                "id": 2,
                "quantity": 90
            }
        ]

    """
    products = InventoryRepository.find_all(db)
    return [InventoryResponse.from_orm(product) for product in products]

# Check by id [GET]
@app.get("/inventory/check/{id_inventory}", summary="Shows the quantity of the product from the inventory with the specified id", status_code=200, tags=["Inventory"], response_model=InventoryResponse)
async def check_inventory_by_id(id: int, db: Session = Depends(get_db)):
    """

        Check a product in inventory by its ID if it exists, returns the following inventory product attributes:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        {
        
            "id": 1,
            "quantity": 4
        
        }

    """
    product_in_inventory(db, id)
    product = InventoryRepository.find_by_id(db, id)
    return InventoryResponse.from_orm(product)

# Create Product [POST]
@app.post("/inventory/create", response_model = InventoryResponse, summary= "Add a product to inventory", status_code=201, tags=["Inventory"])
async def add_product(request: InventoryRequest, db: Session = Depends(get_db)):
    """

        Add a product to inventory with the following information, if there still isn't any of it in inventory:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        {
        
            "id": 1,
            "quantity": 4
        
        }

    """
    product = Inventory(**request.dict())
    if InventoryRepository.exists_by_id(db, product.id):
        raise HTTPException(
            status_code=409,
            detail="Product already in inventory! Try to increase or decrease its quantity in movements."
        )
    product = InventoryRepository.add(db, product)
    return InventoryResponse.from_orm(product)

# Update product quantity [PUT]
@app.put("/inventory/update/{id_inventory}", response_model=InventoryResponse, status_code=200, tags=["Inventory"])
async def update_inventory(id: int, request: InventoryRequest, db: Session = Depends(get_db)):
    """

        Update the quantity of a product in inventory by its ID if it exists, returns the following updated product attributes:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        {
        
            "id": 1,
            "quantity": 20
        
        }

    """
    product_in_inventory(db, id)
    product = InventoryRepository.add(db, Inventory(id=id, **request.dict()))
    return InventoryResponse.from_orm(product)

# Remove product from inventory [DELETE]
@app.delete("/inventory/remove/{id_inventory}", status_code=status.HTTP_204_NO_CONTENT, tags=["Inventory"])
async def remove_inventory(id: int, db: Session = Depends(get_db)):
    """

        Remove a product from inventory by ID, no return.

    """
    product_in_inventory(db, id)
    InventoryRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------- MOVEMENTS -------------------------------------------------

# Check movements [GET]
@app.get("/movements/check", summary= "Shows all the products available in the inventory", status_code=200, tags=["Movements"], response_model=list[MovementResponse])
async def check_movements(db: Session = Depends(get_db)):
    """

        Check the movements of the products in inventory, returns a list of the movements of products in inventory. Each movement has the following attributes:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        [

            {
                "id": 1,
                "quantity": 4
            },
            {
                "id": 5,
                "quantity": 6
            },
            {
                "id": 2,
                "quantity": 90
            }
        ]

    """
    movements = MovementRepository.find_all(db)
    return [MovementResponse.from_orm(movement) for movement in movements]

# Check by id [GET]
@app.get("/movements/check/{id_movement}", summary="Shows the quantity of the product from the inventory with the specified id", status_code=200, tags=["Movements"], response_model=MovementResponse)
async def check_movement_by_id(id: int, db: Session = Depends(get_db)):
    """

        Check a product in inventory by its ID if it exists, returns the following inventory product attributes:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        {
        
            "id": 1,
            "quantity": 4
        
        }

    """
    product_in_inventory(db, id)
    product = MovementRepository.find_by_id(db, id)
    return MovementResponse.from_orm(product)

# Create Product [POST]
@app.post("/movements/create", response_model = MovementResponse, summary= "Add a product to inventory", status_code=201, tags=["Movements"])
async def add_movement(request: MovementRequest, db: Session = Depends(get_db)):
    """

        Add a product to inventory with the following information, if there still isn't any of it in inventory:
        - **id**: product ID
        - **quantity**: quantity available in inventory

        Return example:

        {
        
            "id": 1,
            "quantity": 4
        
        }

    """
    product = Movement(**request.dict())
    if MovementRepository.exists_by_id(db, product.id):
        raise HTTPException(
            status_code=409,
            detail="Product already in inventory! Try to increase or decrease its quantity in movements."
        )
    product = MovementRepository.add(db, product)
    return MovementResponse.from_orm(product)