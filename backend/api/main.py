from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from backend.db.database import SessionLocal, engine
from backend.db.models import Base, AdPerformance
from backend.core.utils import read_and_validate_csv
from backend.db.crud import insert_ads
from backend.api.insights import generate_insights
from backend.ml.ml_model import predict_performance
from backend.core.schemas import PredictionInput, PredictionOutput

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ad Performance Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-data")
def upload_data(file: UploadFile, db: Session = Depends(get_db)):
    try:
        logger.info("Upload endpoint called")

        df = read_and_validate_csv(file.file)
        insert_ads(db, df)

        return {"status": "success", "rows_inserted": len(df)}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/insights")
def insights(db: Session = Depends(get_db)):
    records = db.query(AdPerformance).all()
    return {"insights": generate_insights(records)}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    return predict_performance([
        data.impressions,
        data.clicks,
        data.spend,
        data.conversions
    ])
