from fastapi import HTTPException
from uuid import UUID
from src.tasks.dtos import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from src.tasks.models import Task

def create_task(db: Session, task_data: TaskCreate):
    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def list_tasks(db: Session):
    tasks = db.query(Task).all() 
    return tasks

def get_task(db: Session, task_id: UUID):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(db: Session, task_id: UUID, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: UUID):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return task