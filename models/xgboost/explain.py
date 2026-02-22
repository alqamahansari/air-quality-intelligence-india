import pandas as pd
import shap
import matplotlib.pyplot as plt
from xgboost import XGBRegressor

DATA_PATH = "data/processed/aqi_features.csv"


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.sort_values(["city", "date"])

    df = pd.get_dummies(df, columns=["city"], drop_first=True)

    df_model = df.drop(columns=[
        "date",
        "pm25",
        "pm10",
        "no2",
        "so2",
        "co",
        "o3"
    ])

    split_date = df["date"].quantile(0.8)

    train = df_model[df["date"] < split_date]
    test = df_model[df["date"] >= split_date]

    X_train = train.drop(columns=["aqi"])
    y_train = train["aqi"]

    X_test = test.drop(columns=["aqi"])

    model = XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(X_train, y_train)

    explainer = shap.Explainer(model)
    shap_values = explainer(X_test)

    plt.figure()
    shap.summary_plot(shap_values, X_test, show=False)
    plt.tight_layout()
    plt.savefig("models/xgboost/shap_summary.png", dpi=300)

print("SHAP summary saved.")


if __name__ == "__main__":
    main()