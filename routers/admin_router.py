from fastapi import APIRouter, status, Depends, HTTPException, Path
from database import SessionLocal
from models import TODO
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import Path
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dp_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(current_user: user_dependency, db:dp_dependency):
    
    if current_user is None or current_user.role != 'admin':
        return HTTPException(status_code=401, detail="Authentication fails")
    return db.query(TODO).all()


@router.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    current_user: user_dependency,
    db: dp_dependency,
    todo_id: int = Path(..., gt=0, description="Todo ID")
):
    
    if current_user is None or current_user.role != 'admin':
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todo = db.query(TODO).filter(TODO.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
        