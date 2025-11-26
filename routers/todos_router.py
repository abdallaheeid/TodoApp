from fastapi import APIRouter, status, Depends, HTTPException, Path
from database import engine, SessionLocal
from models import TODO
import models
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Path
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Checking if the router is running
@router.get("/api/healthchecker")
async def root():
    return {
        "message": "Welcome to FastAPI With SQLAlchemy"
    }

dp_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: Optional[int] = Field(gt=0, lt=6)
    complete: bool = False    
    
@router.get("/api/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(current_user: user_dependency, db: dp_dependency):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todos = db.query(models.TODO).filter(TODO.user_id == current_user.id).all()
    return todos

@router.get("/api/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(current_user: user_dependency,
                         db: dp_dependency, 
                         todo_id: int = Path(..., gt=0, description="The ID of the todo (must be > 0)")):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == current_user.id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo
    

@router.post("/api/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(current_user:user_dependency, 
                      db: dp_dependency, 
                      todo: TodoRequest):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    new_todo = TODO(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
        user_id=current_user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@router.put("/api/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    current_user: user_dependency,
    db: dp_dependency,
    todo: TodoRequest,
    todo_id: int = Path(..., gt=0)
):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    existing_todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == current_user.id).first()

    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.priority = todo.priority
    existing_todo.complete = todo.complete

    db.commit()
    db.refresh(existing_todo)

    return existing_todo

@router.delete("/api/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    current_user: user_dependency,
    db: dp_dependency,
    todo_id: int = Path(..., gt=0, description="Todo ID")
):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == current_user.id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
    
    