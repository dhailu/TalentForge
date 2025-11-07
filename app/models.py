from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class ResumeMetadata(Base):
    __tablename__ = "resume_metadata"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    blob_path = Column(String)
    text_content = Column(String)
    embedding = Column(Vector(1536))
    uploaded_at = Column(TIMESTAMP, server_default=func.now())
