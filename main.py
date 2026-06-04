from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes import analyze, history

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🚀 ResumeIQ API",
    description="""
    ### An AI-powered resume parsing and ATS optimization engine.
    
    This backend parses uploaded PDF resumes, matches them against target job descriptions using the Google Gemini Pro SDK, caches structural evaluations via Redis, and logs analytical metrics securely to a PostgreSQL database instance.
    
    **Features:**
    * 📄 **PDF Text Extraction:** Clean, inline tokenization of unstructured text.
    * 🤖 **Deterministic AI Schema:** Strict validation using Gemini structured responses.
    * ⚡ **High-Performance Caching:** 24-hour cache invalidation windows via Upstash Redis.
    * 📊 **Persistent Audit Logs:** Historical access endpoints for relational tracking.
    """,
    version="1.0.0",
    contact={
        "name": "Faizan Khan",
        "url": "https://github.com/Faizan-Khan0007",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, tags=["Core Analysis Engine"])
app.include_router(history.router, tags=["Analytics & History"])

@app.get("/health", tags=["System Monitoring"])
def health_check():
    return {
        "status": "online",
        "message": "ResumeIQ backend is running smoothly!"
    }