from fastapi import FastAPI, APIRouter, status, Depends, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import TODO
import models
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Path

app = FastAPI(title="Todos App using FastAPI")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Checking if the app is running
@app.get("/api/healthchecker")
async def root():
    return {
        "message": "Welcome to FastAPI With SQLAlchemy"
    }

dp_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: Optional[int] = Field(gt=0, lt=6)
    complete: bool = False    
    
@app.get("/api/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: dp_dependency):
    todos = db.query(models.TODO).all()
    return todos

@app.get("/api/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: dp_dependency, 
                         todo_id: int = Path(..., gt=0, description="The ID of the todo (must be > 0)")):
    todo = db.query(TODO).filter(TODO.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo
    

@app.post("/api/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: dp_dependency, todo: TodoRequest):
    new_todo = TODO(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@app.put("/api/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: dp_dependency,
    todo: TodoRequest,
    todo_id: int = Path(..., gt=0)
):
    existing_todo = db.query(TODO).filter(TODO.id == todo_id).first()

    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.priority = todo.priority
    existing_todo.complete = todo.complete

    db.commit()
    db.refresh(existing_todo)

    return existing_todo

@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    db: dp_dependency,
    todo_id: int = Path(..., gt=0, description="Todo ID")
):
    todo = db.query(TODO).filter(TODO.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
    
    