import pandas as pd

def clean_youtube():
    # 1. Load the NEW Synthetic Dataset
    # Ensure this file is in your data/raw/ folder!
    df = pd.read_csv("data/raw/youtube_synthetic.csv")

    # 2. Rename Columns
    df = df.rename(columns={
        "trending_date": "Date",
        "video_id": "Campaign_ID",
        "views": "Impressions",
        "likes": "Clicks"
    })

    # 3. Standardize Date
    # Since the synthetic file uses standard YYYY-MM-DD, this now works automatically
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 4. FEATURE ENGINEERING (Crucial for ML!)
    # Adds the same features as Google & Meta so they can be merged
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Day"] = df["Date"].dt.day

    # 5. Numeric Conversions
    df["Impressions"] = pd.to_numeric(df["Impressions"], errors="coerce")
    df["Clicks"] = pd.to_numeric(df["Clicks"], errors="coerce")

    # 6. Add Missing Metrics (YouTube doesn't have Spend/Revenue)
    df["Spend"] = 0.0
    df["Conversions"] = 0.0
    df["Revenue"] = 0.0
    df["Platform"] = "YouTube"

    # 7. Select Final Columns (Matches Unified Schema)
    final_cols = [
        "Date", "Month", "DayOfWeek", "Day",
        "Platform", "Campaign_ID",
        "Impressions", "Clicks", "Spend",
        "Conversions", "Revenue"
    ]

    df = df[final_cols]
    
    # 8. Handle Missing Values
    df.fillna(0, inplace=True)

    # 9. Save
    df.to_csv("data/clean/youtube_clean.csv", index=False)
    print(f"YouTube dataset cleaned successfully. Rows: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    clean_youtube()