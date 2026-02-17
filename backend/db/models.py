from sqlalchemy import Column, Integer, Float, Date
from backend.db.database import Base

class AdPerformance(Base):
    __tablename__ = "ad_performance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    spend = Column(Float, nullable=False)
    conversions = Column(Integer, nullable=False)
    ctr = Column(Float, nullable=False)
    cpc = Column(Float, nullable=False)
    cpa = Column(Float, nullable=False)
