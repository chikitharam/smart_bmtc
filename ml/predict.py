import os
import joblib
import pandas as pd

def predict_demand(route_id, hour, is_weekend, month, is_holiday, event_nearby, prev_passengers, capacity, day_of_week_str):
    # Load from exact 'ml' folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'demand_model.pkl')
    model = joblib.load(model_path)
    
    features = {
        'route_id': route_id,
        'hour': hour,
        'is_weekend': is_weekend,
        'month': month,
        'is_holiday': is_holiday,
        'event_nearby': event_nearby,
        'prev_passengers': prev_passengers,
        'capacity': capacity,
        'day_of_week_Monday': 0,
        'day_of_week_Saturday': 0,
        'day_of_week_Sunday': 0,
        'day_of_week_Thursday': 0,
        'day_of_week_Tuesday': 0,
        'day_of_week_Wednesday': 0
    }
    
    if f'day_of_week_{day_of_week_str}' in features:
        features[f'day_of_week_{day_of_week_str}'] = 1
        
    input_df = pd.DataFrame([features])
    predicted_count = model.predict(input_df)[0]
    
    occupancy_pct = (predicted_count / capacity) * 100
    
    if occupancy_pct <= 40:
        status = "LOW"
    elif occupancy_pct <= 70:
        status = "MODERATE"
    elif occupancy_pct <= 90:
        status = "HIGH"
    else:
        status = "VERY HIGH"
        
    return int(predicted_count), round(occupancy_pct, 2), status

if __name__ == "__main__":
    print("--- BMTC AI Demand Prediction ---")
    pred_passengers, pred_occupancy, demand_level = predict_demand(
        route_id=1, hour=8, is_weekend=0, month=11, is_holiday=0, event_nearby=0, 
        prev_passengers=45, capacity=50, day_of_week_str="Monday"
    )
    print(f"Predicted passengers: {pred_passengers}")
    print(f"Predicted occupancy: {pred_occupancy}%")
    print(f"Demand level: {demand_level}")