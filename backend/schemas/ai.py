# backend/schemas/ai.py
from pydantic import BaseModel

class AIPredictRequest(BaseModel):
    route_id: int
    hour: int
    day_of_week: int  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    previous_demand: int
    capacity: int

class AIPredictResponse(BaseModel):
    route: str
    predicted_passengers: int
    predicted_occupancy: float
    demand_level: str