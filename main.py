from fastapi import FastAPI
from database import engine
from routers import auth_router, todos_router
import models

app = FastAPI(title="Todos App using FastAPI")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(todos_router.router)
