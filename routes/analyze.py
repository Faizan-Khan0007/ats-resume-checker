from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import AnalysisResponse
from services.pdf_service import extract_text_from_pdf, validate_pdf
from services.ai_service import analyze_resume_with_ai
from services.cache_service import generate_cache_key, get_cached_analysis, set_cached_analysis

# Create a router specifically for analysis endpoints
router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume_endpoint(
    job_role: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Validate the file type
    if not validate_pdf(file.filename, file.content_type):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 2. Extract Text
    try:
        raw_bytes = await file.read()
        resume_text = extract_text_from_pdf(raw_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {str(e)}")

    # 3. Check Redis Cache
    cache_key = generate_cache_key(resume_text, job_role)
    cached_result = get_cached_analysis(cache_key)

    if cached_result:
        # We have a cache hit! Return instantly, completely skipping the AI.
        return AnalysisResponse(
            analysis_id=0, # 0 means it wasn't a new DB entry
            cached=True,
            data=cached_result
        )

    # 4. Cache Miss -> Call Gemini AI
    try:
        ai_result = analyze_resume_with_ai(resume_text, job_role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 5. Save the text and metadata to PostgreSQL
    new_resume = models.Resume(
        filename=file.filename,
        extracted_text=resume_text,
        job_role=job_role
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    # 6. Save the AI insights to PostgreSQL, linked to the resume
    new_analysis = models.Analysis(
        resume_id=new_resume.id,
        ats_score=ai_result.ats_score,
        skills_found=ai_result.skills_found,
        skills_missing=ai_result.skills_missing,
        suggestions=ai_result.suggestions,
        keyword_match_percentage=ai_result.keyword_match_percentage
        # Note: We aren't saving the complex exotic features to the DB to keep it lightweight, 
        # but they are sent back to the frontend right below!
    )
    db.add(new_analysis)
    db.commit()

    # 7. Save the full AI result to Redis for the next 24 hours
    set_cached_analysis(cache_key, ai_result)

    # 8. Send the final response to the user
    return AnalysisResponse(
        analysis_id=new_analysis.id,
        cached=False,
        data=ai_result
    )