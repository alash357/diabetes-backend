from sqlalchemy.orm import Session
from app.models.prediction_model import Prediction
from app.schemas.prediction_schema import PredictionInput

def save_prediction(db: Session, user_id: int, prediction: int, data: PredictionInput):
    pred = Prediction(**data.dict(), prediction=prediction, user_id=user_id)
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred

def get_all_predictions(db: Session):
    return db.query(Prediction).all()

def get_user_predictions(db: Session, user_id: int):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()
