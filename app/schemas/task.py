# app/schemas/task.py

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    done: bool = False

class TaskOut(TaskCreate):
    id: int

    class Config:
        orm_mode = True
