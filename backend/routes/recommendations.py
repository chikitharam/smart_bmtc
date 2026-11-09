# backend/routes/recommendations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User, Route, Bus, BusRoute
from schemas import ReallocationResponse
from routes.auth import get_current_admin
from routes.ai import get_predicted_occupancy

router = APIRouter(prefix="/recommendations", tags=["AI Operations"])

@router.get("/bus-allocation/{high_route_id}", response_model=ReallocationResponse)
def get_bus_allocation_recommendation(
    high_route_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    # 1. Fetch the High Demand Route
    high_route = db.query(Route).filter(Route.id == high_route_id).first()
    if not high_route:
        raise HTTPException(status_code=404, detail="High demand route not found")

    # 2. Calculate occupancy for the High Route
    high_occupancy = get_predicted_occupancy(high_route.id, db, hour=8, day_of_week=0)

    # 3. Automatically find the route with the LOWEST demand
    all_other_routes = db.query(Route).filter(Route.id != high_route_id).all()
    
    if not all_other_routes:
        raise HTTPException(status_code=400, detail="No other routes exist in the system to compare against.")

    low_route = None
    lowest_occupancy = 100.0

    for route in all_other_routes:
        occ = get_predicted_occupancy(route.id, db, hour=8, day_of_week=0)
        if occ < lowest_occupancy:
            lowest_occupancy = occ
            low_route = route

    # 4. Apply Rule-Based Logic
    recommendation = ""
    action_required = ""
    suggested_bus = None
    suggested_bus_id = None # <-- Initialize ID

    if high_occupancy > 90 and lowest_occupancy < 40:
        recommendation = f"Route {high_route.route_number} is overcrowded ({high_occupancy}%). Route {low_route.route_number} is underutilized ({lowest_occupancy}%)."
        
        buses_on_low_route = db.query(BusRoute).filter(BusRoute.route_id == low_route.id).all()
        
        if len(buses_on_low_route) > 1: 
            bus_to_move = db.query(Bus).join(BusRoute).filter(BusRoute.route_id == low_route.id).first()
            if bus_to_move:
                suggested_bus = bus_to_move.bus_number
                suggested_bus_id = bus_to_move.id # <-- Store the actual ID
                action_required = f"REVIEW: Consider reallocating bus {suggested_bus} from {low_route.route_number} to {high_route.route_number}."
            else:
                action_required = f"REVIEW: Reallocate one available bus from {low_route.route_number} to {high_route.route_number}."
        else:
            action_required = f"CAUTION: Cannot reallocate from {low_route.route_number} as it only has 1 bus. Consider using a reserve bus."

    elif high_occupancy > 90:
        recommendation = f"Route {high_route.route_number} is overcrowded ({high_occupancy}%)."
        action_required = f"INCREASE FREQUENCY: Deploy an available reserve bus to {high_route.route_number}."
    
    else:
        recommendation = f"Route {high_route.route_number} is operating within optimal demand levels ({high_occupancy}%)."
        action_required = "NO ACTION REQUIRED."

    return {
        "status": "success",
        "high_demand_route": high_route.route_number,
        "high_route_occupancy": high_occupancy,
        "low_demand_route": low_route.route_number,
        "low_route_occupancy": lowest_occupancy,
        "recommendation": recommendation,
        "action_required": action_required,
        "suggested_bus_to_move": suggested_bus,
        "suggested_bus_id": suggested_bus_id, # <-- Return ID
        "high_route_id": high_route.id,       # <-- Return High Route ID
        "low_route_id": low_route.id          # <-- Return Low Route ID
    }