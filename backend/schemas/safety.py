# backend/schemas/safety.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SafetyReportCreate(BaseModel):
    bus_id: Optional[int] = None
    route_id: Optional[int] = None
    report_type: str
    description: str

class SafetyReportResponse(BaseModel):
    id: int
    bus_id: Optional[int] = None
    route_id: Optional[int] = None
    report_type: str
    description: str
    status: str
    created_at: datetime
    # Notice: user_id is intentionally omitted for privacy

    class Config:
        from_attributes = True

class SafetyReportStatusUpdate(BaseModel):
    status: str # OPEN, INVESTIGATING, RESOLVED