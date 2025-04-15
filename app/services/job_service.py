from typing import List, Optional
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobUpdate, Job
from app.models.job import JobStatus


class JobService:
    def __init__(self, repository: JobRepository):
        self.repository = repository

    def get_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        return self.repository.get_jobs(skip, limit)

    def get_job(self, job_id: int) -> Optional[Job]:
        return self.repository.get_job_by_id(job_id)

    def create_job(self, job: JobCreate) -> Job:
        return self.repository.create_job(job)

    def update_job(self, job_id: int, job_update: JobUpdate) -> Optional[Job]:
        return self.repository.update_job(job_id, job_update)

    def delete_job(self, job_id: int) -> bool:
        return self.repository.delete_job(job_id)

    def get_jobs_by_status(self, status: JobStatus, skip: int = 0, limit: int = 100) -> List[Job]:
        return self.repository.get_jobs_by_status(status, skip, limit)