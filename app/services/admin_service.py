from sqlalchemy.orm import Session
from app.models.prediction_model import Prediction

def merge_temp_predictions(db: Session):
    temp_data = db.query(Prediction).filter(Prediction.source == "temp").limit(1000).all()
    for item in temp_data:
        item.source = "main"
    db.commit()
    return {"merged": len(temp_data)}

def get_all_predictions(db: Session):
    return db.query(Prediction).order_by(Prediction.created_at.desc()).all()
