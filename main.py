from fastapi import FastAPI
from src.utils.settings import settings
from src.utils.db import get_db, Base, engine
from src.tasks.models import Task
from src.tasks.router import task_router
from src.users.models import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", description="API for managing tasks", version="1.0.0")
app.include_router(task_router)