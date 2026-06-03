import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Read DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,      # Tests the connection before every single query
    pool_recycle=300,        # Recycles connections every 5 minutes to avoid sudden drops
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)#creates connection

# Base model class
Base = declarative_base() #a parent class for tables


# Open / close DB session
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()