# backend/schemas/card.py
from pydantic import BaseModel
from typing import Optional

class CardResponse(BaseModel):
    id: int
    card_number: str
    status: str
    user_id: int
    wallet_balance: float = 0.0