from fastapi import FastAPI
from backend.services.predictor import predict_latest

app = FastAPI(title="Air Quality Intelligence API")


@app.get("/")
def home():
    return {"message": "Air Quality Intelligence API is running"}


@app.get("/forecast/{city}")
def forecast(city: str):
    return predict_latest(city)