import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Takes raw file bytes from an uploaded PDF, extracts all text, 
    cleans up the whitespace, and returns a single string.
    """
    try:
        # Load the bytes into a PDF reader object
        pdf_file = io.BytesIO(file_bytes) #converted files to a virtual file because pdfreader reads a file object not bytes
        reader = PdfReader(pdf_file)
        
        extracted_text = ""
        
        # Loop through every page and grab the text
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
        # Clean up the text: replace multiple spaces/newlines with a single space
        clean_text = " ".join(extracted_text.split())
        
        if not clean_text:
            raise ValueError("The PDF appears to be empty or contains only images.")
            
        return clean_text
        
    except Exception as e:
        # If anything goes wrong (corrupted file, wrong format), catch it
        raise ValueError(f"Failed to parse PDF: {str(e)}")

def validate_pdf(filename: str, content_type: str) -> bool:
    """
    Checks if the uploaded file is actually a PDF before we try to process it.
    """
    if not filename.lower().endswith('.pdf'):
        return False
    if content_type != 'application/pdf':
        return False
    return True