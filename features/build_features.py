import pandas as pd
import os

INPUT_PATH = "data/processed/aqi_master.csv"
OUTPUT_PATH = "data/processed/aqi_features.csv"


def create_time_features(df):
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_year"] = df["date"].dt.dayofyear
    return df


def create_lag_features(df):
    lag_days = [1, 3, 7]

    for lag in lag_days:
        df[f"aqi_lag_{lag}"] = df.groupby("city")["aqi"].shift(lag)
        df[f"pm25_lag_{lag}"] = df.groupby("city")["pm25"].shift(lag)

    return df


def create_rolling_features(df):
    df["aqi_roll_7"] = (
        df.groupby("city")["aqi"]
        .rolling(7)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return df


def main():
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])

    df = df.sort_values(["city", "date"])

    df = create_time_features(df)
    df = create_lag_features(df)
    df = create_rolling_features(df)

    # Drop rows created due to lag/rolling NaNs
    df = df.dropna()

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Feature dataset shape:", df.shape)
    print("Missing values:\n", df.isnull().sum())


if __name__ == "__main__":
    main()