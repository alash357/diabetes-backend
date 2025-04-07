# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

# Base attributes shared across user schemas
class UserBase(BaseModel):
    email: EmailStr

# Input schema for user registration
class UserCreate(UserBase):
    password: str

# Output schema for user response
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User used for dependency injection (e.g. current_user)
class User(UserOut):
    pass
