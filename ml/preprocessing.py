import pandas as pd
import os
from sklearn.model_selection import train_test_split

def load_and_preprocess_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, 'dataset', 'passenger_demand.csv')
    
    df = pd.read_csv(filepath)
    df = pd.get_dummies(df, columns=['day_of_week'], drop_first=True)
    
    features = [
        'route_id', 'hour', 'is_weekend', 'month', 
        'is_holiday', 'event_nearby', 'prev_passengers', 'capacity'
    ] + [col for col in df.columns if 'day_of_week_' in col]
    
    X = df[features]
    y = df['passengers']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, features