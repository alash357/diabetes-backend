from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.core.database import Base

class TempPrediction(Base):
    __tablename__ = "temp_predictions"

    id = Column(Integer, primary_key=True, index=True)
    glucose = Column(Float)
    bmi = Column(Float)
    age = Column(Float)
    prediction = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
