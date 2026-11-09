# backend/routes/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from database import get_db
from models import User, Card, Bus, Journey
from routes.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/overview")
def get_admin_overview(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    total_passengers = db.query(User).filter(User.role == 'passenger').count()
    active_cards = db.query(Card).filter(Card.status == 'active').count()
    total_buses = db.query(Bus).count()
    total_journeys = db.query(Journey).filter(Journey.status == 'COMPLETED').count()
    
    # Get today's journeys
    today = date.today()
    todays_journeys = db.query(Journey).filter(
        Journey.status == 'COMPLETED', 
        func.date(Journey.start_time) == today
    ).count()

    return {
        "total_passengers": total_passengers,
        "active_cards": active_cards,
        "total_buses": total_buses,
        "total_journeys": total_journeys,
        "todays_journeys": todays_journeys
    }