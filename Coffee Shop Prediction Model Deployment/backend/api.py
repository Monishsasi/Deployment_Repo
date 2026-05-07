from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from predictor import CoffeeRevenuePredictor

app = FastAPI()
predictor = CoffeeRevenuePredictor()

class Input(BaseModel):
    Number_of_Customers_Per_Day: float
    Operating_Hours_Per_Day: float
    Marketing_Spend_Per_Day: float

@app.post("/predict")
def predict(data: Input):
    return {
        "prediction": predictor.predict_single(data.dict())
    }

@app.post("/predict_batch")
def predict_batch(data: list[Input]):
    df = pd.DataFrame([d.dict() for d in data])
    return {
        "predictions": predictor.predict_batch(df)
    }
    