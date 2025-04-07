from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    username: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int
    is_super_admin: bool

    class Config:
        orm_mode = True

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUpdatePassword(BaseModel):
    old_password: str
    new_password: str

class AdminResetPassword(BaseModel):
    email: EmailStr

class AdminResetToken(BaseModel):
    token: str
    new_password: str

class AdminActivityLog(BaseModel):
    admin_id: int
    action: str
    timestamp: Optional[datetime] = None
