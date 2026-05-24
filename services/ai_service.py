import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schemas import ResumeAnalysis

# Load environment variables
load_dotenv()

# Initialize the NEW GenAI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume_with_ai(resume_text: str, job_role: str) -> ResumeAnalysis:
    """
    Sends the parsed resume text to Gemini using the latest GenAI SDK.
    Natively forces a structured JSON response matching our Pydantic schema.
    """
    # Because the new SDK forces the schema directly, our prompt can be much cleaner.
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) and senior tech recruiter.
    Analyze this resume against the target role: {job_role}.
    
    Provide highly actionable, specific feedback. 
    For the line rewrites, choose weak, non-metric-driven bullet points and make them powerful.
    For the keyword strategy, suggest exact sentences they can add to their experience.
    
    RESUME TEXT:
    {resume_text}
    """
    
    try:
        # We are using the newest, fastest model: gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeAnalysis, # <--- MAGIC HAPPENS HERE
                temperature=0.2 # Lower temperature keeps the AI focused and analytical
            ),
        )
        
        # The new SDK automatically parses the JSON back into your Pydantic object!
        if not response.parsed:
            raise ValueError("AI failed to return the structured data.")
            
        return response.parsed
        
    except Exception as e:
        raise ValueError(f"AI Analysis Failed: {str(e)}")