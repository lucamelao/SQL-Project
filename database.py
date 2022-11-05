import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

if database_exists(SQLALCHEMY_DATABASE_URL):
    drop_database(SQLALCHEMY_DATABASE_URL)

create_database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Each instance will be the actual database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create sessions with the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()