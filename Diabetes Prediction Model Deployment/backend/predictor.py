import joblib
import numpy as np

class DiabetesPredictor:
    def __init__(self):
        self.scaler = joblib.load("artifacts/scaler.joblib")
        self.model = joblib.load("artifacts/svm_model.joblib")

    def predict(self, data: list):
        data = np.array(data, dtype=float).reshape(1, -1)
        scaled = self.scaler.transform(data)
        prediction = self.model.predict(scaled)
        return int(prediction[0])
