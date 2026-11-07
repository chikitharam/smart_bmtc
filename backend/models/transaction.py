# backend/models/transaction.py
from sqlalchemy import Column, Integer, Numeric, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(Enum('topup', 'payment', 'refund'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    wallet = relationship("Wallet", back_populates="transactions")