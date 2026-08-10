import os
import json
from groq import Groq
from dotenv import load_dotenv
from schemas import ResumeAnalysis

# Load environment variables
load_dotenv()

# Initialize the Groq client
# It automatically looks for GROQ_API_KEY in the environment
client = Groq()

def analyze_resume_with_ai(resume_text: str, job_role: str) -> ResumeAnalysis:
    """
    Sends the parsed resume text to Groq API.
    Forces a structured JSON response matching our Pydantic schema.
    """
    
    # We must explicitly tell Groq the JSON schema we want
    json_schema_example = {
        "ats_score": 85,
        "keyword_match_percentage": 90,
        "skills_found": ["Python", "FastAPI"],
        "skills_missing": ["Docker", "Kubernetes"],
        "suggestions": ["Add more metrics", "Include Docker experience"],
        "line_rewrites": [
            {
                "original_line": "Built a backend system.",
                "why_its_weak": "Lacks specific metrics and technologies.",
                "rewritten_options": ["Architected a Python FastAPI backend supporting 10k+ daily requests."]
            }
        ],
        "keyword_strategies": [
            {
                "missing_keyword": "Docker",
                "where_to_add": "Experience section under project X",
                "example_sentence": "Containerized the FastAPI backend using Docker to ensure consistent environments."
            }
        ],
        "verb_analysis": {
            "weak_verbs_found": ["helped", "did", "worked"],
            "strong_verb_suggestions": ["spearheaded", "architected", "optimized"]
        }
    }

    prompt = f"""
    You are an expert ATS (Applicant Tracking System) and senior tech recruiter.
    Analyze this resume against the target role: {job_role}.
    
    Provide highly actionable, specific feedback. 
    For the line rewrites, choose weak, non-metric-driven bullet points and make them powerful.
    For the keyword strategy, suggest exact sentences they can add to their experience.
    
    IMPORTANT: You must return ONLY a raw JSON object that exactly matches this schema structure. Do not wrap it in markdown block quotes (```json) or add any other text.
    
    SCHEMA TEMPLATE:
    {json.dumps(json_schema_example, indent=2)}
    
    RESUME TEXT:
    {resume_text}
    """
    
    try:
        # We are using Llama 3.3 70B Versatile for high intelligence and speed
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        
        # Get the raw JSON string returned by Groq
        raw_json_string = chat_completion.choices[0].message.content
        
        # Parse it straight into our Pydantic object to guarantee structure
        parsed_data = ResumeAnalysis.model_validate_json(raw_json_string)
        
        return parsed_data
        
    except Exception as e:
        raise ValueError(f"Groq AI Analysis Failed: {str(e)}")