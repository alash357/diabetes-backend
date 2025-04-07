from fastapi import APIRouter, Depends
from app.core import security
from app.schemas import user_schema

router = APIRouter()

@router.get("/me")
def get_user_data(current_user: user_schema.User = Depends(security.get_current_user)):
    return current_user
