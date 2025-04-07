# app/models/prediction_model.py

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    pregnancies = Column(Integer, nullable=False)
    glucose = Column(Float, nullable=False)
    blood_pressure = Column(Float, nullable=False)
    skin_thickness = Column(Float, nullable=False)
    insulin = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    diabetes_pedigree_function = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)

    prediction = Column(Integer, nullable=False)  # 0 or 1
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")
