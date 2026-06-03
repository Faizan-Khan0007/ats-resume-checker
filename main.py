from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes import analyze, history

# This single line tells SQLAlchemy to create all tables defined in models.py!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ResumeIQ API",
    description="AI-powered resume analyzer backend",
    version="1.0.0"
)
# Crucial for frontend: allow your HTML pages to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# connecting the analyze route
app.include_router(analyze.router)
app.include_router(history.router)

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "message": "ResumeIQ backend is running smoothly!"
    }