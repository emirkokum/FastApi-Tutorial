from fastapi import APIRouter, HTTPException, Depends
from app.models.task import TaskDb
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from app.dependencies import get_db
from app.schemas.task import TaskOut, TaskCreate, TaskUpdate


router = APIRouter(
    prefix="/tasks", #this will be the prefix for all routes in this router
    tags=["Tasks"] #this will be title for swagger documentation
)

@router.get("/",response_model=list[TaskOut])
def list_tasks(db : Session = Depends(get_db)):
    try:
        tasks = db.query(TaskDb).all()
        return tasks
    except SQLAlchemyError as e:
        db.rollback()
        raise 

@router.get("/{task_id}", response_model=TaskOut)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(TaskDb).filter(TaskDb.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise 


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate, db:Session = Depends(get_db)):
    try:
        task = TaskDb(**task.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise 
    
@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    try:
        task = db.query(TaskDb).filter(TaskDb.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )
        
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        
        db.commit()
        db.refresh(task)
        return task

    except SQLAlchemyError as e:
        db.rollback()
        raise 
    

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(TaskDb).filter(TaskDb.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )
        db.delete(task)
        db.commit()
        return 
    except SQLAlchemyError as e:
        db.rollback()
        raise 