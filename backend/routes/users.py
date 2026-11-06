# backend/routes/users.py
from fastapi import APIRouter, Depends
from models import User
from schemas import UserResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get the profile of the currently logged-in passenger."""
    return current_user