from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import models
from .database import engine
from .routers import users, tasks, qa

# Create all tables in the database on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="QA Task Manager API")

# Enable CORS (allow all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(qa.router)

# Mount Static Files
app.mount("/static", StaticFiles(directory="docs"), name="static")

# Health Check Endpoint
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is healthy and running"}
