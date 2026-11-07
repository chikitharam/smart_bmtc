# backend/models/__init__.py
from .user import User
from .card import Card
from .wallet import Wallet
from .transport import Bus, Route, Stop, RouteStop, BusRoute
from .journey import Journey  # <-- Add this
from .transaction import Transaction # <-- Add this