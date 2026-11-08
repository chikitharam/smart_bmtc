# backend/schemas/analytics.py
from pydantic import BaseModel
from typing import List

class RouteDemand(BaseModel):
    route_number: str
    passenger_count: int

class StopDemand(BaseModel):
    stop_name: str
    passenger_count: int

class HourlyDemand(BaseModel):
    hour: int
    passenger_count: int

class DayTypeDemand(BaseModel):
    day_type: str  # "Weekday" or "Weekend"
    passenger_count: int

class BusOccupancyResponse(BaseModel):
    bus_id: int
    bus_number: str
    capacity: int
    current_passengers: int
    occupancy_percentage: float
    status: str
    data_source: str = "Estimated (Digital Tap Data)"