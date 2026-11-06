# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, get_db, Base
import models # We will create models in Day 4, but importing it sets up the Base

# Create all tables in the database (if they don't exist)
# Note: Since we already created them in Workbench, this won't duplicate them.
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart BMTC API",
    description="Backend API for the Smart BMTC System",
    version="1.0.0"
)

@app.get("/")
def home():
    """Basic health check endpoint."""
    return {
        "message": "Smart BMTC Backend Running"
    }

@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint to verify that FastAPI can successfully connect to MySQL.
    It executes a simple 'SELECT 1' query.
    """
    try:
        # Execute a raw SQL query to test the connection
        result = db.execute(text("SELECT 1"))
        # Fetch the first row
        row = result.fetchone()
        
        if row and row[0] == 1:
            return {
                "status": "success",
                "message": "Successfully connected to MySQL database 'smartbmtc'!"
            }
    except Exception as e:
        # If connection fails, return a 500 error with the exception message
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")