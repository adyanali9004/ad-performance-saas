import pandas as pd

def clean_google():
    # 1. Load Data
    df = pd.read_csv("data/raw/GoogleAds_DataAnalytics_Sales_Uncleaned.csv")

    # 2. Rename Columns
    df = df.rename(columns={
        "Ad_Date": "Date",
        "Campaign_Name": "Campaign_ID",
        "Cost": "Spend",
        "Sale_Amount": "Revenue"
    })

    # 3. FIX: Clean Currency (Remove '$' and ',')
    for col in ["Spend", "Revenue"]:
        df[col] = df[col].astype(str).str.replace('$', '', regex=False)
        df[col] = df[col].str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. FIX: Handle Mixed Date Formats (The crucial part!)
    # format='mixed' allows pandas to switch between YYYY-MM-DD and DD-MM-YYYY automatically
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format='mixed', errors='coerce')

    # Drop rows where Date is still missing (if any), instead of filling with 0
    df = df.dropna(subset=['Date'])

    # 5. Add ML Features (Month, Day, DayOfWeek)
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Day"] = df["Date"].dt.day

    # 6. Numeric Conversions
    df["Impressions"] = pd.to_numeric(df["Impressions"], errors="coerce")
    df["Clicks"] = pd.to_numeric(df["Clicks"], errors="coerce")
    df["Conversions"] = pd.to_numeric(df["Conversions"], errors="coerce")
    
    df["Platform"] = "Google"

    # 7. Select Final Columns
    final_cols = [
        "Date", "Month", "DayOfWeek", "Day",
        "Platform", "Campaign_ID",
        "Impressions", "Clicks", "Spend",
        "Conversions", "Revenue"
    ]
    df = df[final_cols]

    # 8. Handle Missing Values
    # Fill numeric columns with 0, but NOT the Date column
    numeric_cols = ["Impressions", "Clicks", "Spend", "Conversions", "Revenue"]
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # 9. Save
    df.to_csv("data/clean/google_clean.csv", index=False)
    print(f"Google dataset cleaned successfully. Rows: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    clean_google()