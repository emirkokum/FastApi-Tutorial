from fastapi import FastAPI
from app.routes import task
from app.database import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions import sqlalchemy_exception_handler, general_exception_handler

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}