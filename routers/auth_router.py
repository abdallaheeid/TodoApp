from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from database import SessionLocal
from typing_extensions import Annotated
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    authenticate_user)

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
    email: str
    first_name: str 
    last_name: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str
    

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
    

@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_db)):

    if not authenticate_user(db, data.username, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    user = db.query(User).filter(User.username == data.username).first()

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    token = create_access_token({"sub": user.username}, timedelta(minutes=20))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "name": f"{current_user.first_name} {current_user.last_name}",
        "active": current_user.is_active
    }