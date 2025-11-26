from fastapi import APIRouter, status, Depends, HTTPException, Path
from database import SessionLocal
from models import TODO, User
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import Path
from .auth import get_current_user, hash_password, verify_password
from pydantic import BaseModel, Field

router = APIRouter(prefix="/user", tags=["user"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dp_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    current_password: str = Field(min_length=4)
    new_password: str = Field(min_length=4)
    confirm_password: str = Field(min_length=4)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(current_user: user_dependency, db:dp_dependency):
    
    if current_user is None:
        return HTTPException(status_code=401, detail="Authentication fails")
    return db.query(User).filter(User.id == current_user.id).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    current_user: user_dependency,
    db: dp_dependency,
    user_verification: UserVerification):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    if not verify_password(user_verification.current_password, current_user.hashed_pass):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if user_verification.new_password != user_verification.confirm_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    current_user.hashed_pass = hash_password(user_verification.new_password)

    db.commit()
    
    return
        