# backend/routes/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List

from database import get_db
from models import User, Journey, Route, Stop, Bus
from schemas import RouteDemand, StopDemand, HourlyDemand, DayTypeDemand, BusOccupancyResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/total-passengers")
def get_total_passengers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns the total number of completed journeys across the entire system."""
    total = db.query(func.count(Journey.id)).filter(Journey.status == 'COMPLETED').scalar()
    return {"total_completed_journeys": total}

@router.get("/route-demand", response_model=List[RouteDemand])
def get_route_demand(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Number of passengers per route."""
    results = db.query(
        Route.route_number,
        func.count(Journey.id).label("passenger_count")
    ).join(Journey, Journey.route_id == Route.id)\
     .filter(Journey.status == 'COMPLETED')\
     .group_by(Route.route_number)\
     .order_by(func.count(Journey.id).desc()).all()
    
    return [{"route_number": r[0], "passenger_count": r[1]} for r in results]

@router.get("/popular-routes", response_model=List[RouteDemand])
def get_popular_routes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Most frequently used routes (Top 5)."""
    results = db.query(
        Route.route_number,
        func.count(Journey.id).label("passenger_count")
    ).join(Journey, Journey.route_id == Route.id)\
     .filter(Journey.status == 'COMPLETED')\
     .group_by(Route.route_number)\
     .order_by(func.count(Journey.id).desc())\
     .limit(5).all()
    
    return [{"route_number": r[0], "passenger_count": r[1]} for r in results]

@router.get("/stop-demand")
def get_stop_demand(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Number of passengers per boarding stop and destination stop."""
    # Boarding stops
    boarding = db.query(
        Stop.stop_name,
        func.count(Journey.id).label("passenger_count")
    ).join(Journey, Journey.boarding_stop_id == Stop.id)\
     .filter(Journey.status == 'COMPLETED')\
     .group_by(Stop.stop_name)\
     .order_by(func.count(Journey.id).desc()).all()

    # Destination stops
    destination = db.query(
        Stop.stop_name,
        func.count(Journey.id).label("passenger_count")
    ).join(Journey, Journey.destination_stop_id == Stop.id)\
     .filter(Journey.status == 'COMPLETED')\
     .group_by(Stop.stop_name)\
     .order_by(func.count(Journey.id).desc()).all()

    return {
        "popular_boarding_stops": [{"stop_name": r[0], "passenger_count": r[1]} for r in boarding],
        "popular_destination_stops": [{"stop_name": r[0], "passenger_count": r[1]} for r in destination]
    }

@router.get("/hourly-demand", response_model=List[HourlyDemand])
def get_hourly_demand(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Number of passengers per hour (extracted from start_time)."""
    # func.hour() extracts the hour (0-23) from the datetime
    results = db.query(
        func.hour(Journey.start_time).label("hour"),
        func.count(Journey.id).label("passenger_count")
    ).filter(Journey.status == 'COMPLETED')\
     .group_by("hour")\
     .order_by("hour").all()
    
    return [{"hour": r[0], "passenger_count": r[1]} for r in results]

@router.get("/weekday-weekend", response_model=List[DayTypeDemand])
def get_weekday_vs_weekend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compares travel volume on Weekdays (Mon-Fri) vs Weekends (Sat-Sun)."""
    # MySQL DAYOFWEEK(): 1 = Sunday, 2 = Monday, ..., 7 = Saturday
    # We use a case statement to bucket days 2-6 as Weekday, and 1 & 7 as Weekend
    day_type = case(
        (func.dayofweek(Journey.start_time).in_([2, 3, 4, 5, 6]), 'Weekday'),
        else_='Weekend'
    ).label('day_type')

    results = db.query(
        day_type,
        func.count(Journey.id).label("passenger_count")
    ).filter(Journey.status == 'COMPLETED')\
     .group_by(day_type).all()

    return [{"day_type": r[0], "passenger_count": r[1]} for r in results]

@router.get("/buses/{bus_id}/occupancy", response_model=BusOccupancyResponse)
def get_bus_occupancy(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculates the estimated real-time occupancy of a specific bus."""
    # 1. Fetch the bus to get its capacity
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # 2. Count active journeys (passengers currently on board)
    active_passengers = db.query(Journey).filter(
        Journey.bus_id == bus_id,
        Journey.status == 'IN_PROGRESS'
    ).count()

    # 3. Calculate Percentage
    if bus.capacity == 0:
        percentage = 0.0
    else:
        percentage = (active_passengers / bus.capacity) * 100

    # 4. Determine Status Category
    if percentage <= 40:
        status = "Low"
    elif percentage <= 70:
        status = "Moderate"
    elif percentage <= 90:
        status = "High"
    else:
        status = "Very High"

    return {
        "bus_id": bus.id,
        "bus_number": bus.bus_number,
        "capacity": bus.capacity,
        "current_passengers": active_passengers,
        "occupancy_percentage": round(percentage, 2),
        "status": status,
        "data_source": "Estimated (Digital Tap Data)"
    }