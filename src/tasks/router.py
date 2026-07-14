from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.tasks import controller
from src.utils.db import get_db
from src.tasks.dtos import TaskCreate, TaskUpdate, TaskRead, ResponseModel

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/create", response_model=ResponseModel)
def create_task(task_data: TaskCreate, db=Depends(get_db)):
    new_task = controller.create_task(db, task_data)
    return {"status": "success", "task": new_task}

@task_router.get("/", response_model=list[TaskRead])
def list_tasks(db=Depends(get_db)):
    return controller.list_tasks(db)

@task_router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID, db=Depends(get_db)):
    return controller.get_task(db, task_id)

@task_router.patch("/update/{task_id}", response_model=ResponseModel)
def update_task(task_id: UUID, task_data: TaskUpdate, db=Depends(get_db)):
    task = controller.update_task(db, task_id, task_data)
    return {"status": "success", "task": task}

@task_router.delete("/delete/{task_id}", response_model=ResponseModel)
def delete_task(task_id: UUID, db=Depends(get_db)):
    task = controller.delete_task(db, task_id)
    return {"status": "success", "task": task}
