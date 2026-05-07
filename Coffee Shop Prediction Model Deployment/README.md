
# ☕ Coffee Shop Revenue Predictor

A simple machine learning application that predicts daily revenue for a coffee shop based on:
- Number of customers
- Operating hours
- Marketing spend

This project uses:
- **FastAPI** for the backend ML inference API  
- **Streamlit** for the frontend UI  
- **Docker & Docker Compose** for easy local deployment  
- **Joblib** to load the trained model and scaler

---

## 🚀 Features

- Single prediction UI
- Batch CSV prediction
- FastAPI endpoints for:
  - `/predict`
  - `/predict_batch`
- Fully containerized (frontend + backend)

---

## 📂 Project Structure

```

project/
│
├── backend/
│   ├── api.py
│   ├── predictor.py
│   ├── requirements.txt
│   └── artifacts/
│       ├── model.joblib
│       └── scaler.joblib
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
└── docker-compose.yml

````

---

## 🐳 Run with Docker Compose

Make sure Docker is installed, then run:

```
docker compose up --build
```

---

## ✨ Tech Used

* Python 3.10+
* FastAPI
* Streamlit
* Docker
* Joblib
* Pandas / NumPy

---

## 🤝 Contributions

Feel free to open issues or PRs if you want to extend this project!

---


