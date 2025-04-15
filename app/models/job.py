from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class JobStatus(str, enum.Enum):
    INTERESTED = "interested"
    APPLIED = "applied"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFER = "offer"
    ACCEPTED = "accepted"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    url = Column(String)
    description = Column(String, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.INTERESTED)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    tags = relationship("Tag", secondary="job_tags", back_populates="jobs")
    owner = relationship("User", back_populates="jobs")