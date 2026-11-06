# backend/routes/cards.py
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User, Card, Wallet
from schemas import CardResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/cards", tags=["Smart Cards"])

def generate_card_number(db: Session) -> str:
    """Generates a unique BMTC card number (e.g., BMTC123456)."""
    while True:
        # Generate a random 6-digit number
        random_digits = random.randint(100000, 999999)
        card_num = f"BMTC{random_digits}"
        # Check if it already exists in the DB
        if not db.query(Card).filter(Card.card_number == card_num).first():
            return card_num

@router.post("/create", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Check if the user already has a card
    existing_card = db.query(Card).filter(Card.user_id == current_user.id, Card.status != 'expired').first()
    if existing_card:
        raise HTTPException(status_code=400, detail="User already has an active smart card")

    # 2. Generate Card Number
    new_card_number = generate_card_number(db)

    # 3. Create the Card
    new_card = Card(
        card_number=new_card_number,
        user_id=current_user.id,
        status="active"
    )
    db.add(new_card)

    # 4. Ensure Wallet exists (create with ₹250 welcome balance for testing)
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=250.00)
        db.add(wallet)

    db.commit()
    db.refresh(new_card)
    db.refresh(wallet)

    return CardResponse(
        id=new_card.id,
        card_number=new_card.card_number,
        status=new_card.status,
        user_id=new_card.user_id,
        wallet_balance=float(wallet.balance)
    )

@router.get("/my-card", response_model=CardResponse)
def get_my_card(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch the active card for the current user
    card = db.query(Card).filter(Card.user_id == current_user.id, Card.status != 'expired').first()
    if not card:
        raise HTTPException(status_code=404, detail="No active smart card found")
    
    # Fetch wallet balance
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    balance = float(wallet.balance) if wallet else 0.0

    return CardResponse(
        id=card.id,
        card_number=card.card_number,
        status=card.status,
        user_id=card.user_id,
        wallet_balance=balance
    )

@router.get("/{card_id}", response_model=CardResponse)
def get_card_by_id(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Security check: Ensure the user is the owner or an admin
    if card.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to view this card")

    wallet = db.query(Wallet).filter(Wallet.user_id == card.user_id).first()
    balance = float(wallet.balance) if wallet else 0.0

    return CardResponse(
        id=card.id,
        card_number=card.card_number,
        status=card.status,
        user_id=card.user_id,
        wallet_balance=balance
    )

@router.put("/{card_id}/block", response_model=CardResponse)
def block_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    if card.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to block this card")
    
    if card.status == 'blocked':
        raise HTTPException(status_code=400, detail="Card is already blocked")

    card.status = 'blocked'
    db.commit()
    db.refresh(card)

    wallet = db.query(Wallet).filter(Wallet.user_id == card.user_id).first()
    balance = float(wallet.balance) if wallet else 0.0

    return CardResponse(
        id=card.id,
        card_number=card.card_number,
        status=card.status,
        user_id=card.user_id,
        wallet_balance=balance
    )