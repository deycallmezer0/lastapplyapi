from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association table for many-to-many relationship
job_tags = Table(
    "job_tags",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    jobs = relationship("Job", secondary=job_tags, back_populates="tags")