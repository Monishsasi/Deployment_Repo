# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from predictor import DiabetesPredictor

app = FastAPI()

# Load ML predictor only once
predictor = DiabetesPredictor()

class DiabetesInput(BaseModel):
    features: list  # list of 8 diabetes input values

@app.post("/predict")
def predict(data: DiabetesInput):
    result = predictor.predict(data.features)
    return {"prediction": result}
