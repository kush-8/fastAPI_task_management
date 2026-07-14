from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.utils.db import get_db
from src.tasks.dtos import TaskCreate, TaskResponse, TaskUpdate
from src.users.models import User
from src.utils.helpers import is_authenticated

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return controller.create_task(db, task_data, user)


@task_router.get("/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return controller.list_tasks(db, user)


@task_router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: UUID, db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return controller.get_task(db, task_id, user)


@task_router.patch("/update/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: UUID, task_data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return controller.update_task(db, task_id, task_data, user)


@task_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return controller.delete_task(db, task_id, user)
