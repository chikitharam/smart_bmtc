# backend/schemas/transport.py
from pydantic import BaseModel
from typing import List

# Bus Schemas
class BusCreate(BaseModel):
    bus_number: str
    capacity: int

class BusResponse(BusCreate):
    id: int
    status: str
    class Config:
        from_attributes = True

# Stop Schemas
class StopCreate(BaseModel):
    stop_name: str
    latitude: float
    longitude: float

class StopResponse(StopCreate):
    id: int
    class Config:
        from_attributes = True

# Route Schemas
class RouteCreate(BaseModel):
    route_number: str
    source: str
    destination: str

class RouteResponse(RouteCreate):
    id: int
    class Config:
        from_attributes = True

# RouteStop Schemas
class RouteStopCreate(BaseModel):
    stop_id: int
    stop_order: int

# To display a route with its stops
class RouteStopResponse(BaseModel):
    stop_order: int
    stop: StopResponse
    class Config:
        from_attributes = True

class RouteWithStopsResponse(RouteResponse):
    stops: List[RouteStopResponse] = []