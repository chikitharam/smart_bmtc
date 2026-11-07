# backend/routes/journeys.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from database import get_db
from routes.auth import get_current_user
from utils.fare import calculate_distance, calculate_fare
from models import User, Card, BusRoute, RouteStop, Journey, Wallet, Stop, Transaction
from schemas import TapInRequest, TapOutRequest, JourneyResponse

router = APIRouter(prefix="/journeys", tags=["Journeys"])

@router.post("/tap-in", response_model=JourneyResponse, status_code=status.HTTP_201_CREATED)
def tap_in(
    request: TapInRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Verify card exists
    card = db.query(Card).filter(Card.card_number == request.card_number).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # Security check: Ensure the card belongs to the logged-in user
    if card.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This card does not belong to you")

    # 2. Check card status
    if card.status != 'active':
        raise HTTPException(status_code=400, detail=f"Card is {card.status}. Cannot tap in.")

    # 3. Check passenger has no other active journey
    active_journey = db.query(Journey).filter(
        Journey.user_id == current_user.id, 
        Journey.status == 'IN_PROGRESS'
    ).first()
    if active_journey:
        raise HTTPException(status_code=400, detail="You already have an active journey. Please tap out first.")

    # 4. Validate bus and route assignment
    bus_route = db.query(BusRoute).filter(
        BusRoute.bus_id == request.bus_id, 
        BusRoute.route_id == request.route_id
    ).first()
    if not bus_route:
        raise HTTPException(status_code=400, detail="This bus is not assigned to the selected route")

    # 5. Validate boarding stop belongs to route
    route_stop = db.query(RouteStop).filter(
        RouteStop.route_id == request.route_id,
        RouteStop.stop_id == request.boarding_stop_id
    ).first()
    if not route_stop:
        raise HTTPException(status_code=400, detail="Boarding stop does not belong to this route")

    # 6 & 7. Record boarding time and create IN_PROGRESS journey
    new_journey = Journey(
        user_id=current_user.id,
        card_id=card.id,
        bus_id=request.bus_id,
        route_id=request.route_id,
        boarding_stop_id=request.boarding_stop_id,
        start_time=datetime.utcnow(),
        status='IN_PROGRESS'
    )

    db.add(new_journey)
    db.commit()
    db.refresh(new_journey)

    return new_journey


@router.post("/tap-out", response_model=JourneyResponse)
def tap_out(
    request: TapOutRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Find the active journey
    journey = db.query(Journey).filter(
        Journey.user_id == current_user.id,
        Journey.status == 'IN_PROGRESS'
    ).first()

    if not journey:
        raise HTTPException(status_code=400, detail="No active journey found. Please tap in first.")

    # 2. Verify the bus matches
    if journey.bus_id != request.bus_id:
        raise HTTPException(status_code=400, detail="You are trying to tap out on a different bus than you boarded.")

    # 3. Validate Destination Stop belongs to the Route
    dest_route_stop = db.query(RouteStop).filter(
        RouteStop.route_id == journey.route_id,
        RouteStop.stop_id == request.destination_stop_id
    ).first()

    if not dest_route_stop:
        raise HTTPException(status_code=400, detail="Destination stop does not belong to this route")

    # 4. Validate Destination is AFTER Boarding Stop
    board_route_stop = db.query(RouteStop).filter(
        RouteStop.route_id == journey.route_id,
        RouteStop.stop_id == journey.boarding_stop_id
    ).first()

    if dest_route_stop.stop_order <= board_route_stop.stop_order:
        raise HTTPException(status_code=400, detail="Destination must be after the boarding stop")

    # 5. Calculate Fare based on Distance
    boarding_stop = db.query(Stop).filter(Stop.id == journey.boarding_stop_id).first()
    destination_stop = db.query(Stop).filter(Stop.id == request.destination_stop_id).first()
    distance = calculate_distance(
        boarding_stop.latitude, boarding_stop.longitude,
        destination_stop.latitude, destination_stop.longitude
    )
    total_fare = calculate_fare(distance)

    # 6. Validate Wallet Balance
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.balance < total_fare:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient balance. Fare is ₹{total_fare}, but you only have ₹{wallet.balance}. Please recharge."
        )

        # 7. ATOMIC TRANSACTION: Deduct balance, create transaction record, complete journey
    try:
        # Deduct Wallet
        wallet.balance -= total_fare
        
        # Create Transaction Log
        new_tx = Transaction(
            wallet_id=wallet.id,
            amount=total_fare,
            type='payment'
        )
        db.add(new_tx)
        
        # Flush to generate the new_tx.id before committing
        db.flush() 

        # Update Journey
        journey.destination_stop_id = request.destination_stop_id
        journey.end_time = datetime.utcnow()
        journey.fare = total_fare
        journey.status = 'COMPLETED'
        journey.transaction_id = new_tx.id  # Link the transaction!

        # Commit all changes
        db.commit()
        db.refresh(journey)
        return journey

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction failed. Journey not completed.")