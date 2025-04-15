from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate, JobUpdate


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        return self.db.query(Job).offset(skip).limit(limit).all()

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def create_job(self, job: JobCreate) -> Job:
        db_job = Job(**job.dict())
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job

    def update_job(self, job_id: int, job_update: JobUpdate) -> Optional[Job]:
        db_job = self.get_job_by_id(job_id)
        if db_job:
            update_data = job_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_job, key, value)
            self.db.commit()
            self.db.refresh(db_job)
        return db_job

    def delete_job(self, job_id: int) -> bool:
        db_job = self.get_job_by_id(job_id)
        if db_job:
            self.db.delete(db_job)
            self.db.commit()
            return True
        return False

    def get_jobs_by_status(self, status: JobStatus, skip: int = 0, limit: int = 100) -> List[Job]:
        return self.db.query(Job).filter(Job.status == status).offset(skip).limit(limit).all()