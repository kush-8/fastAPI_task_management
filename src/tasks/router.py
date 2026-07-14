from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.utils.db import get_db
from src.tasks.dtos import TaskCreate, TaskResponse, TaskUpdate

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return controller.create_task(db, task_data)


@task_router.get("/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(db: Session = Depends(get_db)):
    return controller.list_tasks(db)


@task_router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    return controller.get_task(db, task_id)


@task_router.patch("/update/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: UUID, task_data: TaskUpdate, db: Session = Depends(get_db)):
    return controller.update_task(db, task_id, task_data)


@task_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    return controller.delete_task(db, task_id)
