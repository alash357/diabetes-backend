from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.models import user_model
from app.schemas import auth_schema, user_schema
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    get_current_admin,
)
from datetime import timedelta
from app.core.email_service import send_reset_email_background

router = APIRouter()

@router.post("/register", response_model=user_schema.UserOut)
def register(user_in: auth_schema.RegisterForm, db: Session = Depends(get_db)):
    existing_user = db.query(user_model.User).filter(
        (user_model.User.email == user_in.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    hashed_password = get_password_hash(user_in.password)
    new_user = user_model.User(
        email=user_in.email,
        password=hashed_password,
        name=user_in.name,
        role=user_in.role or "user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=auth_schema.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(user_model.User).filter(user_model.User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(
    request: auth_schema.ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=10))
    background_tasks.add_task(send_reset_email_background, user.email, token)
    return {"msg": "Reset password email sent."}

@router.post("/reset-password")
def reset_password(
    form: auth_schema.ResetPasswordForm,
    db: Session = Depends(get_db)
):
    payload = decode_access_token(form.token)
    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_id = int(payload.get("sub"))
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = get_password_hash(form.new_password)
    db.commit()
    return {"msg": "Password reset successful."}

@router.get("/admin/me", response_model=user_schema.UserOut)
def get_admin_info(
    current_user: user_model.User = Depends(get_current_admin),
):
    return current_user
