import pandas as pd
import numpy as np
import os

# Define file paths
CLEAN_DIR = "data/clean"
FINAL_DIR = "data/final"

FILES = {
    "google": os.path.join(CLEAN_DIR, "google_clean.csv"),
    "meta": os.path.join(CLEAN_DIR, "meta_clean.csv"),
    "youtube": os.path.join(CLEAN_DIR, "youtube_clean.csv")
}

OUTPUT_FILE = os.path.join(FINAL_DIR, "ads_combined_final.csv")

def merge_datasets():
    print("🚀 Starting Pipeline: Merging Datasets...")
    
    # 1. Load Cleaned Datasets
    dfs = []
    for platform, filepath in FILES.items():
        if os.path.exists(filepath):
            print(f"   Reading {platform} data...")
            df = pd.read_csv(filepath)
            dfs.append(df)
        else:
            print(f"⚠️ Warning: {filepath} not found. Skipping {platform}.")
    
    if not dfs:
        print("❌ Error: No data files found to merge.")
        return

    # 2. Concatenate (Stack them on top of each other)
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    
    # 3. Fill NaNs (Just in case)
    # Metric columns should be 0 if missing
    metric_cols = ["Impressions", "Clicks", "Spend", "Conversions", "Revenue"]
    combined_df[metric_cols] = combined_df[metric_cols].fillna(0)
    
    print(f"✅ Merged {len(combined_df)} rows.")

    # 4. FEATURE ENGINEERING: Calculate KPIs
    # We use np.where to avoid Division by Zero errors (e.g., if Impressions is 0)
    
    print("📊 Calculating KPIs (CTR, CPC, CPA, ROAS)...")

    # CTR (Click Through Rate) = (Clicks / Impressions) * 100
    combined_df["CTR"] = np.where(
        combined_df["Impressions"] > 0, 
        (combined_df["Clicks"] / combined_df["Impressions"]) * 100, 
        0
    )

    # CPC (Cost Per Click) = Spend / Clicks
    combined_df["CPC"] = np.where(
        combined_df["Clicks"] > 0, 
        combined_df["Spend"] / combined_df["Clicks"], 
        0
    )

    # CPA (Cost Per Acquisition) = Spend / Conversions
    combined_df["CPA"] = np.where(
        combined_df["Conversions"] > 0, 
        combined_df["Spend"] / combined_df["Conversions"], 
        0
    )

    # ROAS (Return on Ad Spend) = Revenue / Spend
    combined_df["ROAS"] = np.where(
        combined_df["Spend"] > 0, 
        combined_df["Revenue"] / combined_df["Spend"], 
        0
    )

    # 5. Save Final Dataset
    if not os.path.exists(FINAL_DIR):
        os.makedirs(FINAL_DIR)
        
    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"🎉 Success! Final dataset saved to: {OUTPUT_FILE}")
    print(combined_df.head())

if __name__ == "__main__":
    merge_datasets()