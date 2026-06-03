from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from database import get_db
import models
from schemas import HistoryItem

router = APIRouter()

@router.get("/history", response_model=List[HistoryItem])
def get_resume_history(db: Session = Depends(get_db)):
    """Fetches all past resume analyses, sorted by newest first."""
    
    # We query the exact fields our HistoryItem schema expects by joining the two tables
    results = db.query(
        models.Analysis.id,
        models.Resume.filename,
        models.Resume.job_role,
        models.Analysis.ats_score,
        models.Analysis.created_at
    ).join(
        models.Resume, models.Analysis.resume_id == models.Resume.id
    ).order_by(
        desc(models.Analysis.created_at) # Newest at the top
    ).all()
    
    return results