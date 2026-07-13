from fastapi import FastAPI
from src.utils.settings import settings
from src.utils.db import get_db, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", description="API for managing tasks", version="1.0.0")