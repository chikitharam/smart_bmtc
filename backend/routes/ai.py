# backend/routes/ai.py
import os
import joblib
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Route, User
from schemas import AIPredictRequest, AIPredictResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Predictions"])

# Safely find the root folder and load the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "demand_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ ML Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading ML Model at {MODEL_PATH}: {e}")
    model = None

def get_predicted_occupancy(route_id: int, db: Session, hour: int = 8, day_of_week: int = 0) -> float:
    """Internal helper to get the predicted occupancy percentage for a route."""
    if model is None:
        return 0.0
        
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        return 0.0
        
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_str = days[day_of_week]
    is_weekend = 1 if day_of_week >= 5 else 0

    # To simulate different demands for different routes (since our synthetic data only has Route 1),
    # we adjust the previous_passengers baseline based on the route_id.
    # Route 1 will be high, Route 2 will be low, etc.
    simulated_prev_demand = max(10, 45 - (route_id * 15)) 

    features = {
        'route_id': route_id,
        'hour': hour,
        'is_weekend': is_weekend,
        'month': datetime.now().month,
        'is_holiday': 0,
        'event_nearby': 0,
        'prev_passengers': simulated_prev_demand, # <-- Uses simulated variance
        'capacity': 50,        
        'day_of_week_Monday': 0,
        'day_of_week_Saturday': 0,
        'day_of_week_Sunday': 0,
        'day_of_week_Thursday': 0,
        'day_of_week_Tuesday': 0,
        'day_of_week_Wednesday': 0
    }
    
    if f'day_of_week_{day_str}' in features:
        features[f'day_of_week_{day_str}'] = 1

    try:
        input_df = pd.DataFrame([features])
        predicted_count = int(model.predict(input_df)[0])
        occupancy_pct = (predicted_count / 50) * 100
        return round(occupancy_pct, 2)
    except:
        return 0.0

@router.post("/predict-demand", response_model=AIPredictResponse)
def predict_demand(
    request: AIPredictRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if model is None:
        raise HTTPException(status_code=500, detail="ML Model is not loaded on the server.")

    # Verify Route exists
    route = db.query(Route).filter(Route.id == request.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Map day_of_week integer to strings
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if request.day_of_week < 0 or request.day_of_week > 6:
        raise HTTPException(status_code=400, detail="day_of_week must be between 0 (Mon) and 6 (Sun)")
    
    day_str = days[request.day_of_week]
    is_weekend = 1 if request.day_of_week >= 5 else 0 

    # Build features
    features = {
        'route_id': request.route_id,
        'hour': request.hour,
        'is_weekend': is_weekend,
        'month': datetime.now().month,
        'is_holiday': 0,    
        'event_nearby': 0,  
        'prev_passengers': request.previous_demand,
        'capacity': request.capacity,
        'day_of_week_Monday': 0,
        'day_of_week_Saturday': 0,
        'day_of_week_Sunday': 0,
        'day_of_week_Thursday': 0,
        'day_of_week_Tuesday': 0,
        'day_of_week_Wednesday': 0
    }

    if f'day_of_week_{day_str}' in features:
        features[f'day_of_week_{day_str}'] = 1

    # Predict
    try:
        input_df = pd.DataFrame([features])
        predicted_count = int(model.predict(input_df)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Occupancy calculation
    occupancy_pct = (predicted_count / request.capacity) * 100 if request.capacity > 0 else 0.0
    
    if occupancy_pct <= 40:
        status = "LOW"
    elif occupancy_pct <= 70:
        status = "MODERATE"
    elif occupancy_pct <= 90:
        status = "HIGH"
    else:
        status = "VERY HIGH"

    return {
        "route": route.route_number,
        "predicted_passengers": predicted_count,
        "predicted_occupancy": round(occupancy_pct, 2),
        "demand_level": status
    }