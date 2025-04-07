# backend/app/schemas/predict_schema.py

from pydantic import BaseModel
from datetime import datetime


class PredictionInput(BaseModel):
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree_function: float
    age: int


class PredictionOut(PredictionInput):
    id: int
    prediction: int  # 0 = Non-Diabetic, 1 = Diabetic
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode
