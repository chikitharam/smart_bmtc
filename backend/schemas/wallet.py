# backend/schemas/wallet.py
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import List

class WalletBalanceResponse(BaseModel):
    balance: Decimal

class RechargeRequest(BaseModel):
    amount: Decimal

class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    type: str
    created_at: datetime

    class Config:
        from_attributes = True