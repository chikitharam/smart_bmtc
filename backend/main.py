# backend/main.py
from fastapi import FastAPI
from database import engine, Base
from routes import auth, users, cards # <-- Import cards
from routes import auth, users, cards, transport # <-- Add transport

# This will now automatically create the 'cards' and 'wallets' tables if they don't exist!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart BMTC API",
    description="Backend API for the Smart BMTC System",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cards.router) # <-- Include cards router
app.include_router(transport.router) # <-- Add this

@app.get("/")
def home():
    return {"message": "Smart BMTC Backend Running"}