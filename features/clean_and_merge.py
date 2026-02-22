import os
import pandas as pd
from glob import glob

RAW_PATH = "data/raw/"
OUTPUT_PATH = "data/processed/aqi_master.csv"


def clean_single_file(file_path):
    df = pd.read_csv(file_path)

    # Drop completely empty columns
    df = df.dropna(axis=1, how="all")

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "", regex=False)
        .str.replace(" ", "_")
    )

    if "pm2.5" in df.columns:
        df = df.rename(columns={"pm2.5": "pm25"})

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y", errors="coerce")

    df = df.dropna(subset=["date"])
    df = df.drop_duplicates(subset=["city", "date"])
    df = df.sort_values(["city", "date"])
    # Drop rows where target is missing
    df = df.dropna(subset=["aqi"])
    return df

def merge_all_files():
    all_files = glob(os.path.join(RAW_PATH, "*.csv"))

    if not all_files:
        raise ValueError("No CSV files found in raw directory.")

    dfs = []
    for file in all_files:
        print(f"Processing {file}")
        cleaned = clean_single_file(file)
        dfs.append(cleaned)

    merged_df = pd.concat(dfs, ignore_index=True)

    # Final sorting
    merged_df = merged_df.sort_values(["city", "date"])

    return merged_df


def main():
    os.makedirs("data/processed", exist_ok=True)

    df = merge_all_files()

    print("Final shape:", df.shape)
    print("Missing values summary:\n", df.isnull().sum())

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved cleaned dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


import pandas as pd

df = pd.read_csv("data/processed/aqi_master.csv")

print(df.groupby("city").size())
print(df["date"].min(), "→", df["date"].max())
print(df.describe())