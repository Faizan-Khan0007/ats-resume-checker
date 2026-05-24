from services.pdf_service import extract_text_from_pdf
from services.ai_service import analyze_resume_with_ai

# 1. Read the PDF you used yesterday
file_path = "Faizan_resume.pdf"
job_target = "Software Engineer"

print(f"Reading {file_path}...")
with open(file_path, "rb") as file:
    raw_bytes = file.read()
    
text = extract_text_from_pdf(raw_bytes)
print("PDF read successfully! Sending to Gemini API (This might take 10-15 seconds)...\n")

# 2. Send the text to our new AI service
try:
    result = analyze_resume_with_ai(text, job_target)
    
    print("--- 🧠 AI ANALYSIS SUCCESSFUL 🧠 ---\n")
    print(f"ATS Score: {result.ats_score}/100")
    print(f"Keyword Match: {result.keyword_match_percentage}%\n")
    
    print("Exotic Feature 1: Line Rewrite")
    if result.line_rewrites:
        print(f"Weak Line: {result.line_rewrites[0].original_line}")
        print(f"Fix 1: {result.line_rewrites[0].rewritten_options[0]}\n")
    
    print("Exotic Feature 2: Sneak Strategy")
    if result.keyword_strategies:
        print(f"Missing: {result.keyword_strategies[0].missing_keyword}")
        print(f"How to sneak it in: {result.keyword_strategies[0].example_sentence}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")