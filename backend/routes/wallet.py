# backend/routes/wallet.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Wallet, Transaction
from schemas import WalletBalanceResponse, RechargeRequest, TransactionResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.get("/balance", response_model=WalletBalanceResponse)
def get_balance(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}

@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    # Fetch transactions ordered by newest first
    transactions = db.query(Transaction).filter(Transaction.wallet_id == wallet.id).order_by(Transaction.created_at.desc()).all()
    return transactions

@router.post("/recharge", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def recharge_wallet(
    request: RechargeRequest,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Recharge amount must be greater than zero")

    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    try:
        # 1. Add to balance
        wallet.balance += request.amount

        # 2. Create transaction record
        new_tx = Transaction(
            wallet_id=wallet.id,
            amount=request.amount,
            type='topup'
        )
        db.add(new_tx)
        
        # 3. Commit atomically
        db.commit()
        db.refresh(new_tx)
        return new_tx
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to recharge wallet")