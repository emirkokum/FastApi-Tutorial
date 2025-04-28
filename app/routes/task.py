from fastapi import APIRouter, HTTPException, Depends
from app.models.task import TaskDb
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from app.dependencies import get_db
from app.schemas.task import TaskOut, TaskCreate


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
        # Database error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There is a problem with database."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected Error."
        )

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate, db:Session = Depends(get_db)):
    try:
        db_task = TaskDb(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There is a problem with database."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected Error."
        )