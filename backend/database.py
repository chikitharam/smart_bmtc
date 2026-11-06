# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the database URL from the environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine.
# pool_pre_ping=True helps recover from dropped MySQL connections.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create a SessionLocal class. Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class. Our ORM models (in models/) will inherit from this class.
Base = declarative_base()

# Dependency to get the database session in our routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()