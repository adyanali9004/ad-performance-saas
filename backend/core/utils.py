import pandas as pd
import numpy as np

REQUIRED_COLUMNS = {"date", "impressions", "clicks", "spend", "conversions"}

def read_and_validate_csv(file):
    df = pd.read_csv(file)

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("CSV missing required columns")

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    df = df.dropna(subset=["date"])

    df["ctr"] = np.where(df["impressions"] > 0, df["clicks"] / df["impressions"], 0)
    df["cpc"] = np.where(df["clicks"] > 0, df["spend"] / df["clicks"], 0)
    df["cpa"] = np.where(df["conversions"] > 0, df["spend"] / df["conversions"], 0)

    df.fillna(0, inplace=True)

    return df
