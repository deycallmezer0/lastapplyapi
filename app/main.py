from fastapi import FastAPI
from app.api import jobs
from app.core.database import engine
from app.models import job

# Create the database tables
job.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Tracker API",
    description="API for tracking job applications",
    version="0.1.0"
)

# Include routers
app.include_router(jobs.router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Job Tracker API"}