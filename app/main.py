from fastapi import FastAPI
from routes import task

app = FastAPI()

app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}