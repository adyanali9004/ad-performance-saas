import os
import joblib

MODEL_PATH = "models/model.pkl"
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)

load_model()

def predict_performance(data):
    impressions, clicks, spend, conversions = data

    if model:
        prediction = model.predict([[impressions, clicks, spend, conversions]])
        return {
            "predicted_clicks": int(prediction[0][0]),
            "predicted_conversions": int(prediction[0][1]),
            "predicted_spend_next_30_days": float(prediction[0][2])
        }

    return {
        "predicted_clicks": int(clicks * 1.15),
        "predicted_conversions": int(conversions * 1.2),
        "predicted_spend_next_30_days": round(spend * 30, 2),
        "note": "Using placeholder logic until ML model is integrated"
    }
