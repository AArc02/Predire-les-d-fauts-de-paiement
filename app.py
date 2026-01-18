from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

# Initialize FastAPI app
app = FastAPI(title="Credit Default Prediction API", version="1.0.0")

# Load the trained model and scaler
try:
    model_path = 'best_random_forest_model.joblib'
    scaler_path = 'scaler.joblib'
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    
    best_rf_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("Modèle et Scaler chargés avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle ou du scaler: {e}")
    raise

# Define the input data model using Pydantic
class CreditData(BaseModel):
    LIMIT_BAL: float
    SEX: int
    EDUCATION: int
    MARRIAGE: int
    AGE: int
    PAY_0: int
    PAY_2: int
    PAY_3: int
    PAY_4: int
    PAY_5: int
    PAY_6: int
    BILL_AMT1: float
    BILL_AMT2: float
    BILL_AMT3: float
    BILL_AMT4: float
    BILL_AMT5: float
    BILL_AMT6: float
    PAY_AMT1: float
    PAY_AMT2: float
    PAY_AMT3: float
    PAY_AMT4: float
    PAY_AMT5: float
    PAY_AMT6: float

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Credit Default Prediction API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Verify model and scaler are loaded
        if best_rf_model is None or scaler is None:
            raise HTTPException(status_code=503, detail="Model or scaler not loaded")
        return {
            "status": "healthy",
            "model_loaded": True,
            "scaler_loaded": True
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# Define the /predict endpoint
@app.post("/predict")
async def predict_default(data: CreditData):
    try:
        # Convert input data to a Pandas DataFrame
        input_df = pd.DataFrame([data.dict()])

        # Apply the same preprocessing steps as during training
        # 1. Normalize EDUCATION and MARRIAGE
        input_df['EDUCATION'] = input_df['EDUCATION'].replace([0, 5, 6], 4)
        input_df['MARRIAGE'] = input_df['MARRIAGE'].replace(0, 3)

        # 2. Harmonize payment history values
        pay_columns = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
        for col in pay_columns:
            input_df[col] = input_df[col].replace([-2, -1], 0)

        # 3. Handle categorical encoding (one-hot encoding)
        categorical_cols = ['SEX', 'EDUCATION', 'MARRIAGE']
        
        if hasattr(best_rf_model, 'feature_names_in_'):
            training_columns = best_rf_model.feature_names_in_
        else:
            raise HTTPException(
                status_code=500, 
                detail="Cannot retrieve feature names from the model. Please ensure `feature_names_in_` is available."
            )

        # Create dummy variables for categorical columns (matching training)
        input_df_encoded = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)

        # Ensure all training columns are present, fill missing with 0, and reorder
        missing_cols = set(training_columns) - set(input_df_encoded.columns)
        for c in missing_cols:
            input_df_encoded[c] = 0
        input_df_processed = input_df_encoded[training_columns]

        # 4. Apply StandardScaler to numerical features
        all_numerical_cols_initial = ['LIMIT_BAL', 'AGE', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
        numerical_cols_to_scale_in_input = [col for col in all_numerical_cols_initial if col in input_df_processed.columns]

        if len(numerical_cols_to_scale_in_input) > 0:
            input_df_processed[numerical_cols_to_scale_in_input] = scaler.transform(input_df_processed[numerical_cols_to_scale_in_input])

        # Make prediction
        prediction_proba = best_rf_model.predict_proba(input_df_processed)[:, 1]
        prediction_class = int(best_rf_model.predict(input_df_processed)[0])

        return {
            "prediction": prediction_class,
            "probability_default": float(prediction_proba[0]),
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
