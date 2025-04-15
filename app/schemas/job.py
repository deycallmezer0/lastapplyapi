from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from app.models.job import JobStatus

class JobBase(BaseModel):
    title: str
    company: str
    url: HttpUrl
    description: Optional[str] = None
    notes: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    status: Optional[JobStatus] = None
    notes: Optional[str] = None

class JobInDB(JobBase):
    id: int
    status: JobStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    class Config:
        orm_mode = True



from typing import List

# Add Tag schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

# Update JobCreate
class JobCreate(JobBase):
    tag_ids: Optional[List[int]] = None

# Update Job schemas
class Job(JobInDB):
    tags: List[Tag] = []