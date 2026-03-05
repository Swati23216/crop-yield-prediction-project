import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from .models import Crop

def train_model():
    # Get data from model
    crops = Crop.objects.all().values('name', 'nitrogen', 'phosphorous', 'potash', 'rainfall', 'temperature', 'soil_ph')
    
    if not crops:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(list(crops))
    
    # Features and target
    X = df.drop('name', axis=1)
    y = df['name']
    
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler

def predict_crop(nitrogen, phosphorous, potash, rainfall, temperature, soil_ph):
    model, scaler = train_model()
    
    if model is None:
        return "Not enough data to make a prediction"
    
    # Create input array
    input_data = np.array([[nitrogen, phosphorous, potash, rainfall, temperature, soil_ph]])
    
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(input_scaled)[0]
    
    return prediction