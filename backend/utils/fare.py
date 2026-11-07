# backend/utils/fare.py
import math
from decimal import Decimal

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth 
    using the Haversine formula. Returns distance in kilometers.
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def calculate_fare(distance_km: float) -> Decimal:
    """
    Calculate fare based on distance tiers.
    Returns Decimal to avoid float precision issues with the database.
    """
    if distance_km <= 5:
        return Decimal('5.00')
    elif distance_km <= 10:
        return Decimal('10.00')
    elif distance_km <= 15:
        return Decimal('15.00')
    else:
        return Decimal('20.00')