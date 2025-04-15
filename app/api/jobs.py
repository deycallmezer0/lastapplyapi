from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.job import Job, JobCreate, JobUpdate
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.models.job import JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[Job])
def get_jobs(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        status: JobStatus = None,
        db: Session = Depends(get_db)
):
    repository = JobRepository(db)
    service = JobService(repository)

    if status:
        return service.get_jobs_by_status(status, skip, limit)
    return service.get_jobs(skip, limit)


@router.post("/", response_model=Job, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    repository = JobRepository(db)
    service = JobService(repository)
    return service.create_job(job)


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    repository = JobRepository(db)
    service = JobService(repository)
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=Job)
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    repository = JobRepository(db)
    service = JobService(repository)
    job = service.update_job(job_id, job_update)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    repository = JobRepository(db)
    service = JobService(repository)
    if not service.delete_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return None