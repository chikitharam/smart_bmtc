# backend/schemas/__init__.py
from .user import UserCreate, UserLogin, UserResponse, Token
from .card import CardResponse
from .transport import (
    BusCreate, BusResponse, StopCreate, StopResponse, 
    RouteCreate, RouteResponse, RouteStopCreate, 
    RouteStopResponse, RouteWithStopsResponse
)
#from .journey import TapInRequest, JourneyResponse  # <-- Add this
from .journey import TapInRequest, TapOutRequest, JourneyResponse  # <-- Add TapOutRequest
from .wallet import WalletBalanceResponse, RechargeRequest, TransactionResponse
from .ticket import TicketResponse
from .analytics import RouteDemand, StopDemand, HourlyDemand, DayTypeDemand, BusOccupancyResponse
from .ai import AIPredictRequest, AIPredictResponse
from .recommendation import ReallocationResponse
