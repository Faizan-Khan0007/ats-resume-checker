#schema-> shape of data/structure
from pydantic import BaseModel 
#base model => Smart class + validation + json conversion
from typing import List
from datetime import datetime

# EXOTIC FEATURE SCHEMAS
# These force the AI to provide detailed, 
# actionable data for our unique UI features.

class RewrittenLine(BaseModel):
    original_line: str
    why_its_weak: str
    rewritten_options: List[str]

class ActionVerbAnalysis(BaseModel):
    weak_verbs_found: List[str]
    strong_verb_suggestions: List[str]

class KeywordStrategy(BaseModel):
    missing_keyword: str
    where_to_add: str
    example_sentence: str

# CORE AI OUTPUT SCHEMA (The Gemini Contract)
# Gemini MUST return a JSON object matching this exact shape.

class ResumeAnalysis(BaseModel):
    ats_score: int
    skills_found: List[str]
    skills_missing: List[str]
    suggestions: List[str]
    keyword_match_percentage: int
    
    # Embedding our exotic features
    line_rewrites: List[RewrittenLine]
    verb_analysis: ActionVerbAnalysis
    keyword_strategies: List[KeywordStrategy]

# API ENDPOINT SCHEMAS
# How data moves between our frontend and backend.

# What the frontend sends to us (along with the PDF file)
class AnalyzeRequest(BaseModel):
    job_role: str

# What we send back to the frontend after analysis
class AnalysisResponse(BaseModel):
    analysis_id: int
    cached: bool
    data: ResumeAnalysis

# What we send to the frontend for the History page
class HistoryItem(BaseModel):
    id: int
    filename: str
    job_role: str
    ats_score: int
    created_at: datetime

    # This tells Pydantic to seamlessly read data from our SQLAlchemy models
    model_config = {"from_attributes": True}