from fastapi import FastAPI
from app.routes import task
from app.database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}