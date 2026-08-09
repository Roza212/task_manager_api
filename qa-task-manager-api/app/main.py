from fastapi import FastAPI
from . import models
from .database import engine

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="QA Task Manager API")

@app.get("/")
def read_root():
    return {"message": "API is running"}

