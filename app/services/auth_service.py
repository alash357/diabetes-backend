from app.models.user_model import User
from app.core.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return create_access_token(data={"sub": user.email})
