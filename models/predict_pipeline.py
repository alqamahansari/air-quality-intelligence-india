import pandas as pd
import joblib
from models.health_risk.risk_model import HealthRiskModel

DATA_PATH = "data/processed/aqi_features.csv"
MODEL_PATH = "artifacts/xgb_model.pkl"


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.sort_values(["city", "date"])

    df = pd.get_dummies(df, columns=["city"], drop_first=True)

    # Remove leakage features
    drop_cols = [
        "date",
        "pm25",
        "pm10",
        "no2",
        "so2",
        "co",
        "o3"
    ]

    df = df.drop(columns=drop_cols)

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Use latest row for inference
    latest_sample = df.drop(columns=["aqi"]).iloc[-1:]
    predicted_aqi = model.predict(latest_sample)[0]

    risk_model = HealthRiskModel()

    category = risk_model.get_category(predicted_aqi)
    risk_score = risk_model.get_risk_score(predicted_aqi)
    asthma_risk = risk_model.population_adjusted_risk(predicted_aqi, "asthma")
    advisory = risk_model.advisory_message(category)

    print("Predicted AQI:", round(predicted_aqi, 2))
    print("Category:", category)
    print("Risk Score:", round(risk_score, 2))
    print("Asthma Risk Score:", round(asthma_risk, 2))
    print("Advisory:", advisory)


if __name__ == "__main__":
    main()