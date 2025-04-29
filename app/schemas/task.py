# app/schemas/task.py

from typing import Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    done: bool = False

class TaskOut(TaskCreate):
    id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None