import pandas as pd
import numpy as np
import mlflow
import mlflow.xgboost
import joblib
import os
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = "data/processed/aqi_features.csv"


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.sort_values(["city", "date"])

    # One-hot encode city
    df = pd.get_dummies(df, columns=["city"], drop_first=True)

    split_date = df["date"].quantile(0.8)

    train = df[df["date"] < split_date]
    test = df[df["date"] >= split_date]

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

    train = train.drop(columns=drop_cols)
    test = test.drop(columns=drop_cols)

    X_train = train.drop(columns=["aqi"])
    y_train = train["aqi"]

    X_test = test.drop(columns=["aqi"])
    y_test = test["aqi"]

    with mlflow.start_run():

        model = XGBRegressor(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # Save trained model
        os.makedirs("artifacts", exist_ok=True)
        joblib.dump(model, "artifacts/xgb_model.pkl")

        print("MAE :", round(mae, 2))
        print("RMSE:", round(rmse, 2))
        print("R2  :", round(r2, 4))
        print("Model saved to artifacts/xgb_model.pkl")


if __name__ == "__main__":
    main()