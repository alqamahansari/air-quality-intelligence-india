import pandas as pd
import joblib
from models.health_risk.risk_model import HealthRiskModel

DATA_PATH = "data/processed/aqi_features.csv"
MODEL_PATH = "artifacts/xgb_model.pkl"

# Load once
model = joblib.load(MODEL_PATH)
risk_model = HealthRiskModel()

# Load and prepare dataset once
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df.sort_values(["city", "date"])
df_encoded = pd.get_dummies(df, columns=["city"], drop_first=True)

drop_cols = [
    "date",
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3"
]

df_encoded = df_encoded.drop(columns=drop_cols)

available_cities = df["city"].unique().tolist()


def predict_latest(city: str):

    if city not in available_cities:
        return {"error": f"City not found. Available cities: {available_cities}"}

    city_col = f"city_{city}"

    # Handle base category case (if drop_first=True removed one city)
    if city_col not in df_encoded.columns:
        latest_row = df_encoded[
            ~df_encoded[[col for col in df_encoded.columns if col.startswith("city_")]].any(axis=1)
        ].iloc[-1:]
    else:
        latest_row = df_encoded[df_encoded[city_col] == 1].iloc[-1:]

    X = latest_row.drop(columns=["aqi"])

    predicted_aqi = model.predict(X)[0]

    category = risk_model.get_category(predicted_aqi)
    risk_score = risk_model.get_risk_score(predicted_aqi)
    asthma_risk = risk_model.population_adjusted_risk(predicted_aqi, "asthma")
    advisory = risk_model.advisory_message(category)

    return {
        "predicted_aqi": round(float(predicted_aqi), 2),
        "category": category,
        "risk_score": round(float(risk_score), 2),
        "asthma_risk": round(float(asthma_risk), 2),
        "advisory": advisory
    }