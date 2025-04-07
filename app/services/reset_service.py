import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.email_service import send_password_reset_email

# In-memory token storage for simplicity (can use Redis/DB in prod)
reset_tokens = {}

def generate_reset_token(email: str):
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {"email": email, "expires": datetime.utcnow() + timedelta(minutes=10)}
    send_password_reset_email(email, token)
    return token

def verify_reset_token(token: str):
    token_data = reset_tokens.get(token)
    if not token_data or token_data["expires"] < datetime.utcnow():
        return None
    return token_data["email"]

def reset_password(db: Session, email: str, new_password: str):
    from app.core.security import get_password_hash
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    user.password = get_password_hash(new_password)
    db.commit()
    return user
