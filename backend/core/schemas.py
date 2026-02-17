from pydantic import BaseModel

class PredictionInput(BaseModel):
    impressions: int
    clicks: int
    spend: float
    conversions: int

class PredictionOutput(BaseModel):
    predicted_clicks: int
    predicted_conversions: int
    predicted_spend_next_30_days: float
    note: str | None = None
