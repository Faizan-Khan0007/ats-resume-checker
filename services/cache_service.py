import redis
import hashlib
import json
from schemas import ResumeAnalysis

# Connect to our local Redis server
redis_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def generate_cache_key(resume_text: str, job_role: str) -> str:
    """Creates a unique fingerprint for this specific resume and job role combination."""
    combined_string = f"{resume_text}_{job_role}"
    # Create an MD5 hash of the combined string
    fingerprint = hashlib.md5(combined_string.encode('utf-8')).hexdigest()
    return f"resume_analysis_{fingerprint}"

def get_cached_analysis(cache_key: str):
    """Checks Redis for the cache key. Returns the parsed Pydantic object if found."""
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Convert the raw JSON string back into our Pydantic model
        return ResumeAnalysis.model_validate_json(cached_data)
    return None

def set_cached_analysis(cache_key: str, analysis: ResumeAnalysis):
    """Saves the AI result to Redis for 24 hours (86400 seconds)."""
    # Convert the Pydantic model to a JSON string
    json_data = analysis.model_dump_json()
    redis_client.setex(cache_key, 86400, json_data)