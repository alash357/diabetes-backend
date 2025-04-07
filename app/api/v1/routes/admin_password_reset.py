# app/api/v1/routes/admin_password_reset.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.database import get_db
from app.models.admin_model import Admin
from app.schemas.admin_schema import AdminPasswordResetRequest, AdminPasswordResetConfirm
from app.core.config import settings  # where your SECRET_KEY and ALGORITHM live
from app.utils.email_sender import send_reset_email  # You'll implement this later

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_reset_token(email: str):
    expires = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


@router.post("/password-reset/request", summary="Request password reset")
def request_password_reset(data: AdminPasswordResetRequest, db: Session = Depends(get_db), request: Request = None):
    admin = db.query(Admin).filter(Admin.email == data.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    token = create_reset_token(admin.email)
    frontend_url = settings.FRONTEND_URL or "http://localhost:5173"
    reset_link = f"{frontend_url}/admin/reset-password/{token}"

    # Replace with SendGrid/Mailgun later
    send_reset_email(admin.email, reset_link)

    return {"message": "Reset link sent to your email."}


@router.post("/password-reset/confirm", summary="Confirm password reset")
def confirm_password_reset(data: AdminPasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    hashed_password = pwd_context.hash(data.new_password)
    admin.password = hashed_password
    db.commit()

    return {"message": "Password has been successfully reset."}
