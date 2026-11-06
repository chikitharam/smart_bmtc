# backend/routes/transport.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Bus, Route, Stop, RouteStop, BusRoute, User
from schemas import (
    BusCreate, BusResponse, StopCreate, StopResponse, 
    RouteCreate, RouteResponse, RouteStopCreate, RouteWithStopsResponse
)
from routes.auth import get_current_admin, get_current_user

router = APIRouter(tags=["Transport Management"])

# --- BUS ENDPOINTS ---
@router.post("/buses/", response_model=BusResponse, status_code=status.HTTP_201_CREATED)
def create_bus(bus: BusCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    db_bus = db.query(Bus).filter(Bus.bus_number == bus.bus_number).first()
    if db_bus:
        raise HTTPException(status_code=400, detail="Bus number already exists")
    
    new_bus = Bus(bus_number=bus.bus_number, capacity=bus.capacity)
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus

@router.get("/buses/", response_model=List[BusResponse])
def get_buses(db: Session = Depends(get_db)):
    return db.query(Bus).all()


# --- ROUTE ENDPOINTS ---
@router.post("/routes/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(route: RouteCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    db_route = db.query(Route).filter(Route.route_number == route.route_number).first()
    if db_route:
        raise HTTPException(status_code=400, detail="Route number already exists")
    
    new_route = Route(route_number=route.route_number, source=route.source, destination=route.destination)
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@router.get("/routes/", response_model=List[RouteResponse])
def get_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()


# --- STOP ENDPOINTS ---
@router.post("/stops/", response_model=StopResponse, status_code=status.HTTP_201_CREATED)
def create_stop(stop: StopCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    new_stop = Stop(stop_name=stop.stop_name, latitude=stop.latitude, longitude=stop.longitude)
    db.add(new_stop)
    db.commit()
    db.refresh(new_stop)
    return new_stop


# --- ROUTE-STOP MAPPING ---
@router.post("/routes/{route_id}/stops", status_code=status.HTTP_201_CREATED)
def add_stop_to_route(
    route_id: int, 
    route_stop: RouteStopCreate, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    # Verify route and stop exist
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    stop = db.query(Stop).filter(Stop.id == route_stop.stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")

    # Check if order is already taken
    existing_order = db.query(RouteStop).filter(
        RouteStop.route_id == route_id, 
        RouteStop.stop_order == route_stop.stop_order
    ).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="Another stop already exists at this order")

    new_mapping = RouteStop(route_id=route_id, stop_id=route_stop.stop_id, stop_order=route_stop.stop_order)
    db.add(new_mapping)
    db.commit()
    return {"message": "Stop added to route successfully"}

@router.get("/routes/{route_id}/stops", response_model=RouteWithStopsResponse)
def get_route_stops(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


# --- BUS-ROUTE ASSIGNMENT ---
@router.post("/buses/{bus_id}/assign/{route_id}", status_code=status.HTTP_201_CREATED)
def assign_bus_to_route(
    bus_id: int, 
    route_id: int, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not bus or not route:
        raise HTTPException(status_code=404, detail="Bus or Route not found")

    # Check if already assigned
    existing = db.query(BusRoute).filter(BusRoute.bus_id == bus_id, BusRoute.route_id == route_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bus is already assigned to this route")

    assignment = BusRoute(bus_id=bus_id, route_id=route_id)
    db.add(assignment)
    db.commit()
    return {"message": f"Bus {bus.bus_number} assigned to Route {route.route_number} successfully"}