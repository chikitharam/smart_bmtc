# ml/train_model.py
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocessing import load_and_preprocess_data

def train():
    print("Loading data...")
    X_train, X_test, y_train, y_test, features = load_and_preprocess_data()
    
    print("\n--- Training Random Forest Regressor ---")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model on UNSEEN test data (the 20% split)
    predictions = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    print("\n=============================================")
    print("       MODEL EVALUATION METRICS (TEST DATA)  ")
    print("=============================================")
    print(f"Mean Absolute Error (MAE) : {mae:.2f} passengers")
    print(f"Root Mean Squared Error   : {rmse:.2f} passengers")
    print(f"R-squared (R2) Score      : {r2:.4f}")
    print("=============================================")
    print("Note: MAE and RMSE tell you how many passengers")
    print("the model is typically wrong by. R2 tells you")
    print("how well the model captures the variance.")
    print("=============================================\n")
    
    # Save exactly to the 'ml' folder, not 'ml/dataset'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'demand_model.pkl')
    joblib.dump(model, model_path)
    print(f"✅ Model saved successfully at: {model_path}")

if __name__ == "__main__":
    train()