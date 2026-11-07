# backend/routes/tickets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from database import get_db
from models import User, Journey, Card, Bus, Route, Stop
from schemas import TicketResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/tickets", tags=["Digital Tickets"])

def format_ticket(journey: Journey) -> dict:
    """Helper function to format a Journey model into a TicketResponse dictionary."""
    return {
        "journey_id": journey.id,
        "transaction_id": journey.transaction_id,
        "card_number": journey.card.card_number if journey.card else "N/A",
        "bus_number": journey.bus.bus_number if journey.bus else "N/A",
        "route_number": journey.route.route_number if journey.route else "N/A",
        "from_stop": journey.boarding_stop.stop_name if journey.boarding_stop else "N/A",
        "to_stop": journey.destination_stop.stop_name if journey.destination_stop else "N/A",
        "start_time": journey.start_time,
        "end_time": journey.end_time,
        "fare": journey.fare if journey.fare else 0.0,
        "status": journey.status,
        "qr_data": f"TICKET:{journey.id}|FARE:{journey.fare}|TX:{journey.transaction_id}"
    }

@router.get("/", response_model=List[TicketResponse])
def get_ticket_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a list of all completed journeys (ticket history) for the current user."""
    journeys = db.query(Journey).options(
        joinedload(Journey.card),
        joinedload(Journey.bus),
        joinedload(Journey.route),
        joinedload(Journey.boarding_stop),
        joinedload(Journey.destination_stop)
    ).filter(
        Journey.user_id == current_user.id,
        Journey.status == 'COMPLETED'
    ).order_by(Journey.end_time.desc()).all()

    return [format_ticket(j) for j in journeys]

@router.get("/{journey_id}", response_model=TicketResponse)
def get_ticket_details(
    journey_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific ticket."""
    journey = db.query(Journey).options(
        joinedload(Journey.card),
        joinedload(Journey.bus),
        joinedload(Journey.route),
        joinedload(Journey.boarding_stop),
        joinedload(Journey.destination_stop)
    ).filter(
        Journey.id == journey_id,
        Journey.user_id == current_user.id # Ensure user owns this ticket
    ).first()

    if not journey:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if journey.status != 'COMPLETED':
        raise HTTPException(status_code=400, detail="Ticket is not completed yet")

    return format_ticket(journey)