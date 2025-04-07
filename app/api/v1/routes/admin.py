# app/api/v1/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin
from app.schemas.predict_schema import PredictionOut
from app.models.prediction_model import Prediction

router = APIRouter()

@router.get("/predictions", response_model=List[PredictionOut])
def get_all_predictions(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Retrieve all prediction records (admin-only route).
    """
    try:
        predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).all()
        return predictions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving predictions: {str(e)}"
        )
