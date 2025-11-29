import streamlit as st
import requests
import pandas as pd

st.title("Coffee Revenue Predictor")

API_URL = "http://localhost:8000"  

st.subheader("Single Prediction")

customers = st.number_input("Customers", 100.0)
hours = st.number_input("Operating Hours", 8.0)
marketing = st.number_input("Marketing Spend", 50.0)

if st.button("Predict"):
    data = {
        "Number_of_Customers_Per_Day": customers,
        "Operating_Hours_Per_Day": hours,
        "Marketing_Spend_Per_Day": marketing
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=data).json()
        st.success(f"Predicted Revenue: {response['prediction']}")
    except Exception as e:
        st.error("Backend not reachable")


st.subheader("Batch CSV Prediction")

file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)
    st.write(df)

    if st.button("Batch Predict"):
        try:
            records = df.to_dict(orient="records")
            response = requests.post(f"{API_URL}/predict_batch", json={"records": records}).json()
            df["prediction"] = response["predictions"]
            st.write(df)
        except Exception:
            st.error("Backend not reachable")
