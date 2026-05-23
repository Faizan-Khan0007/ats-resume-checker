from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True) # Will hold the raw PDF text
    job_role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Link to the analysis
    analysis = relationship("Analysis", back_populates="resume", uselist=False)

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    
    # AI Output Data
    ats_score = Column(Integer)
    skills_found = Column(JSON)      # Stores Python lists as JSON
    skills_missing = Column(JSON)
    suggestions = Column(JSON)
    keyword_match_percentage = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Link back to the resume
    resume = relationship("Resume", back_populates="analysis")