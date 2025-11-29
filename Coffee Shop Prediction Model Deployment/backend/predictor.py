import joblib
import numpy as np
import pandas as pd


class CoffeeRevenuePredictor:

    def __init__(self):
        self.model = joblib.load("artifacts/model.joblib")
        self.scaler = joblib.load("artifacts/scaler.joblib")

        self.feature_order = [
            "Number_of_Customers_Per_Day",
            "Operating_Hours_Per_Day",
            "Marketing_Spend_Per_Day"
        ]

    def predict_single(self, features: dict):
        X = np.array([features[f] for f in self.feature_order]).reshape(1, -1)
        X = self.scaler.transform(X)
        return float(self.model.predict(X)[0])

    def predict_batch(self, df: pd.DataFrame):
        df = df[self.feature_order]
        X = self.scaler.transform(df.values)
        return self.model.predict(X).tolist()
