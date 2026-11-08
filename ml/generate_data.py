import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_bmtc_data(num_days=90, route="500D", capacity=50):
    np.random.seed(42)
    data = []
    start_date = datetime(2026, 1, 1)
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.strftime('%A')
        is_weekend = day_of_week in ['Saturday', 'Sunday']
        
        for hour in range(6, 24):
            if 8 <= hour <= 10:
                base_demand = np.random.randint(35, 50)
            elif 17 <= hour <= 19:
                base_demand = np.random.randint(30, 45)
            else:
                base_demand = np.random.randint(10, 30)
            
            if is_weekend:
                base_demand = int(base_demand * 0.4) 
                
            noise = np.random.randint(-5, 6)
            passengers = max(0, min(base_demand + noise, capacity))
            
            data.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "route": route,
                "route_id": 1,
                "hour": hour,
                "day_of_week": day_of_week,
                "is_weekend": 1 if is_weekend else 0,
                "month": current_date.month,
                "is_holiday": 0,
                "event_nearby": 0,
                "passengers": passengers,
                "capacity": capacity
            })
            
    df = pd.DataFrame(data)
    df['prev_passengers'] = df['passengers'].shift(1).fillna(0).astype(int)
    
    # Get current absolute directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(current_dir, 'dataset')
    os.makedirs(dataset_dir, exist_ok=True)
    
    output_path = os.path.join(dataset_dir, 'passenger_demand.csv')
    df.to_csv(output_path, index=False)
    print(f"✅ Dataset generated successfully at {output_path}")
    print(f"Total records: {len(df)}")

if __name__ == "__main__":
    generate_bmtc_data()