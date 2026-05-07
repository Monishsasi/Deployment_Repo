# 🚀 Diabetes Prediction App – Dockerized Deployment

This repository contains the deployment setup for a full-stack Machine Learning application built with FastAPI (backend) and Streamlit (frontend).
Both services are fully containerized using Docker, and orchestrated together using Docker Compose.

## 📌 Project Overview

This setup demonstrates how to package and run a real-time ML application using modern DevOps practices:

**FastAPI Backend:**

- Loads the trained ML model using joblib

- Preprocesses incoming data

- Generates diabetes predictions through an API endpoint

- Exposes clean, sync-ready HTTP endpoints for the frontend

**Streamlit Frontend:**

- Provides an interactive UI for user input

- Sends data to FastAPI for prediction

- Displays the model output instantly

**Dockerized Services:**

- Each service has its own Dockerfile

- Lightweight, scalable, production-ready containers

**Docker Compose Setup:**

- Runs both containers together in a unified environment

- Handles networking between frontend and backend automatically

## 🧩 Features

- Multi-container deployment using Docker Compose

- Separate Dockerfiles for backend and frontend

- Easy setup and portable runtime environment

- Real-time ML inference via FastAPI API

- Streamlit UI connected to backend for predictions

- Clean and modular project structure

## 📁 Repository Structure

📦 deployment-repo
 ├── backend/
 │    ├── Dockerfile
 │    ├── app/
 │    └── artifacts/
 ├── frontend/
 │    ├── Dockerfile
 │    └── app/
 ├── docker-compose.yml
 └── README.md

## 🐳 Run With Docker Compose

Make sure Docker and Docker Compose are installed on your system.

If you want to use the images directly from Docker Hub, first pull them:
```
docker pull monishsasi/diabetes_pred_app:backend
docker pull monishsasi/diabetes_pred_app:frontend
```
then run,

```
docker compose up --build
```

Frontend will be available at:
```
http://localhost:8501
```

Backend will run on:
```
http://localhost:8000
```

## 📦 Docker Images

Images are pushed to Docker Hub for easy access:

Frontend Image: https://hub.docker.com/repository/docker/monishsasi/diabetes_pred_app

Backend Image: https://hub.docker.com/repository/docker/monishsasi/diabetes_pred_app

## 🔗 Useful Links

GitHub Repository: https://github.com/Monishsasi/Deployment_Repo/tree/main/Diabetes%20Prediction%20Model%20Deployment

Docker Hub Images: https://hub.docker.com/repository/docker/monishsasi/diabetes_pred_app

## 🛠️ Tech Stack

- FastAPI

- Streamlit

- Python

- Docker

- Docker Compose

- Machine Learning (scikit-learn model using joblib)

## 🚀 Future Enhancements

- Deploy to cloud (AWS / Azure / GCP)

- Add more ML models

- Scale using container orchestration