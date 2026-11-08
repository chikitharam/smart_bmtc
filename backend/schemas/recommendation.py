# backend/schemas/recommendation.py
from pydantic import BaseModel
from typing import Optional

class ReallocationResponse(BaseModel):
    status: str
    high_demand_route: str
    high_route_occupancy: float
    low_demand_route: str
    low_route_occupancy: float
    recommendation: str
    action_required: str
    suggested_bus_to_move: Optional[str] = None