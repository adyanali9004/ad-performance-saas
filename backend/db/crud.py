from backend.db.models import AdPerformance

def insert_ads(db, df):
    records = []

    for _, row in df.iterrows():
        ad = AdPerformance(
            date=row["date"],
            impressions=int(row["impressions"]),
            clicks=int(row["clicks"]),
            spend=float(row["spend"]),
            conversions=int(row["conversions"]),
            ctr=float(row["ctr"]),
            cpc=float(row["cpc"]),
            cpa=float(row["cpa"])
        )
        records.append(ad)

    db.bulk_save_objects(records)
    db.commit()
