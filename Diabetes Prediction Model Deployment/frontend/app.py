# frontend/app.py
import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/predict")
st.title("Diabetes Predictor")

labels = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]
inputs = [st.number_input(lbl, value=0.0) for lbl in labels]

if st.button("Predict"):
    resp = requests.post(API_URL, json={"features": inputs}, timeout=10)
    st.json(resp.json())
