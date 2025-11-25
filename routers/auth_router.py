from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from models import User
from database import SessionLocal
from typing_extensions import Annotated
from .auth import hash_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dp_dependency = Annotated[Session, Depends(get_db)]

# -------------------- DTOs --------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: str 
    last_name: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

# -------------------- Create User --------------------
@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: dp_dependency):

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_pass=hash_password(user.password),
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }