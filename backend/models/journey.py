# backend/models/journey.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Journey(Base):
    __tablename__ = "journeys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    boarding_stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    destination_stop_id = Column(Integer, ForeignKey("stops.id"), nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    fare = Column(Numeric(10, 2), nullable=True)
    status = Column(Enum('IN_PROGRESS', 'COMPLETED', 'CANCELLED'), default='IN_PROGRESS', nullable=False)
    
    # New relationship for the receipt
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)

    # Relationships
    user = relationship("User")
    card = relationship("Card")
    bus = relationship("Bus")
    route = relationship("Route")
    boarding_stop = relationship("Stop", foreign_keys=[boarding_stop_id])
    destination_stop = relationship("Stop", foreign_keys=[destination_stop_id])
    transaction = relationship("Transaction")