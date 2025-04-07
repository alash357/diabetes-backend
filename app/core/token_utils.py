from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
SECURITY_PASSWORD_SALT = "reset-password-salt"  # you can change it

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_password_reset_token(email: str) -> str:
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def verify_password_reset_token(token: str, expiration: int = 3600) -> str:
    try:
        email = serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=expiration)
        return email
    except Exception:
        return None