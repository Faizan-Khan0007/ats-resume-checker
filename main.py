from fastapi import FastAPI
from database import engine, Base
import models

# This single line tells SQLAlchemy to create all tables defined in models.py!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ResumeIQ API",
    description="AI-powered resume analyzer backend",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "message": "ResumeIQ backend is running smoothly!"
    }