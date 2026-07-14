from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    title: str
    description: str
    completed: bool
