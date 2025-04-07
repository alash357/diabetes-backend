# app/api/v1/routes/predict.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.predict_schema import PredictionInput, PredictionOut
from app.core.database import get_db
from app.models import prediction_model
from app.ml.model_loader import predict_diabetes
from app.core import security

router = APIRouter()

@router.post("/", response_model=PredictionOut, summary="Make a diabetes prediction")
def make_prediction(
    input: PredictionInput,
    db: Session = Depends(get_db),
    current_user=Depends(security.get_current_user),
):
    """
    Run diabetes prediction using the ML model, save the result in the DB,
    and return the prediction record with metadata.
    """
    try:
        result = predict_diabetes(input.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    prediction_record = prediction_model.Prediction(
        user_id=current_user.id,
        prediction=result,
        pregnancies=input.pregnancies,
        glucose=input.glucose,
        blood_pressure=input.blood_pressure,
        skin_thickness=input.skin_thickness,
        insulin=input.insulin,
        bmi=input.bmi,
        diabetes_pedigree_function=input.diabetes_pedigree_function,
        age=input.age,
        created_at=datetime.utcnow(),
    )

    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return prediction_record
