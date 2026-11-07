# backend/schemas/journey.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TapInRequest(BaseModel):
    card_number: str
    bus_id: int
    route_id: int
    boarding_stop_id: int

class TapOutRequest(BaseModel):
    card_number: str
    bus_id: int
    destination_stop_id: int

class JourneyResponse(BaseModel):
    id: int
    user_id: int
    card_id: int
    bus_id: int
    route_id: int
    boarding_stop_id: int
    destination_stop_id: Optional[int] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    fare: Optional[float] = None
    status: str

    class Config:
        from_attributes = True