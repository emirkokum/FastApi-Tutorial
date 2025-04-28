from fastapi import APIRouter, HTTPException
from models.task import Task

router = APIRouter(
    prefix="/tasks", #this will be the prefix for all routes in this router
    tags=["Tasks"] #this will be title for swagger documentation
)

tasks = [
    Task(id=1, title="Alışveriş Yap", description="Marketten ekmek ve süt al", done=False),
    Task(id=2, title="Ödev Yap", description="Matematik ödevi", done=True),
]

@router.get("/",response_model=list[Task])
def list_tasks():
    return tasks


@router.post("/", response_model=Task,status_code=201)
def create_task(task: Task):
    for t in tasks:
        if t.id == task.id:
            return HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

