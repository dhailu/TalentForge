# from sqlalchemy import Column, Integer, String, TIMESTAMP, text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import func
# from pgvector.sqlalchemy import Vector

# Base = declarative_base()
# # Define ResumeMetadata model
# class ResumeMetadata(Base):
#     __tablename__ = "resume_metadata"
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, nullable=False)
#     source_path = Column(String)
#     text_content = Column(String)
#     embedding = Column(Vector(1536))
#     uploaded_at = Column(TIMESTAMP, server_default=func.now())
    
# # Define Embeddings model
# class Embeddings(Base):
#     __tablename__ = "embeddings"
#     id = Column(Integer, primary_key=True, index=True)
#     doc_id = Column(Integer, nullable=False, unique=True)
#     embedding = Column(Vector(1536))
#     created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
