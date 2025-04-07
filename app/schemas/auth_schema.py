# app/schemas/auth_schema.py

from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# For user registration
class RegisterForm(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

# For user login
class LoginForm(BaseModel):
    email: EmailStr
    password: str

# Token returned after login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# For requesting password reset
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# For resetting password
class ResetPasswordForm(BaseModel):
    token: str
    new_password: constr(min_length=6)
