# backend/models/transport.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Bus(Base):
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String(20), unique=True, index=True, nullable=False)
    capacity = Column(Integer, default=0)
    status = Column(Enum('active', 'maintenance', 'inactive'), default='active')

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    route_number = Column(String(20), unique=True, index=True, nullable=False)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    
    # Relationship to get stops for this route
    stops = relationship("RouteStop", back_populates="route", order_by="RouteStop.stop_order")

class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True, index=True)
    stop_name = Column(String(120), nullable=False)
    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)

class RouteStop(Base):
    __tablename__ = "route_stops"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    stop_order = Column(Integer, nullable=False)

    route = relationship("Route", back_populates="stops")
    stop = relationship("Stop")

    # Ensure a route doesn't have duplicate order numbers
    __table_args__ = (UniqueConstraint('route_id', 'stop_order', name='_route_stop_order_uc'),)

class BusRoute(Base):
    __tablename__ = "bus_routes"
    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    bus = relationship("Bus")
    route = relationship("Route")