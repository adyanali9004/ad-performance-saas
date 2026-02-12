import pandas as pd
from datetime import timedelta

def clean_meta():
    # 1. Load Data
    df = pd.read_csv("data/raw/meta_data_synthetic.csv")

    # 2. Rename Columns
    df = df.rename(columns={
        "reporting_start": "Date",
        "campaign_id": "Campaign_ID",
        "spent": "Spend",
        "impressions": "Impressions",
        "clicks": "Clicks",
        "approved_conversion": "Conversions"
    })

    # 3. DATE PARSING & SYNTHETIC SHIFT (The Magic Step!)
    # First, parse the original 2017 dates
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # CALCULATE SHIFT: We want the max date to be Nov 30, 2024 (matching Google)
    # Original max is roughly Aug 30, 2017.
    # We add 2649 days to bring it to Nov 2024.
    target_date = pd.Timestamp("2024-11-30")
    original_max = df["Date"].max()
    
    if pd.notnull(original_max):
        shift_days = target_date - original_max
        print(f"Shifting Meta data by {shift_days.days} days to match 2024 timeline...")
        df["Date"] = df["Date"] + shift_days

    # 4. Feature Engineering (Now these features will match 2024!)
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Day"] = df["Date"].dt.day

    # 5. Numeric Conversions
    for col in ["Impressions", "Clicks", "Spend", "Conversions"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. Platform & Revenue
    df["Platform"] = "Meta"
    df["Revenue"] = 0.0 # Meta doesn't have revenue, so 0

    # 7. Final Columns
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
    df.to_csv("data/clean/meta_clean.csv", index=False)
    print(f"Meta dataset cleaned & shifted successfully. Rows: {len(df)}")
    print(f"New Date Range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(df.head())

if __name__ == "__main__":
    clean_meta()