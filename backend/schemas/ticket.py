# backend/schemas/ticket.py
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class TicketResponse(BaseModel):
    journey_id: int
    transaction_id: Optional[int]
    card_number: str
    bus_number: str
    route_number: str
    from_stop: str
    to_stop: str
    start_time: datetime
    end_time: Optional[datetime]
    fare: Decimal
    status: str
    qr_data: str  # A string the frontend can use to generate a QR code