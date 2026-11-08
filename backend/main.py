# backend/main.py
from fastapi import FastAPI
from database import engine, Base
from routes import auth, users, cards, transport, journey, wallet, tickets, analytics, ai, recommendations# <-- Add journeys
from fastapi.staticfiles import StaticFiles # <-- Add this
from fastapi.responses import FileResponse # <-- Add this

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
app.include_router(journey.router) # <-- Add this
app.include_router(wallet.router)
app.include_router(tickets.router) # <-- Add this
app.include_router(analytics.router) # <-- Add this
app.include_router(ai.router) # <-- Add this
app.include_router(recommendations.router) # <-- Add this

# Mount the static folder to serve HTML/CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add a route to easily open the scanner page
@app.get("/scanner")
def serve_scanner():
    return FileResponse("static/scanner.html")

@app.get("/")
def home():
    return {"message": "Smart BMTC Backend Running"}
