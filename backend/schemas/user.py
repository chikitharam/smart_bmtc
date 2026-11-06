# backend/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema for registering a new user
class UserCreate(BaseModel):
    name: str
    email: EmailStr # Pydantic automatically validates if it's a real email format
    phone: str
    password: str

# Schema for logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for returning user data (Notice: no password field!)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    created_at: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models

# Schema for the JWT Token response
class Token(BaseModel):
    access_token: str
    token_type: str