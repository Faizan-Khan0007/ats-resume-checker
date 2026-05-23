from services.pdf_service import extract_text_from_pdf

# Put a real PDF in your project folder and name it my_resume.pdf
file_path = "Faizan_resume.pdf"

try:
    print(f"Reading {file_path}...")
    
    # Open the PDF in binary read mode ('rb')
    with open(file_path, "rb") as file:
        raw_bytes = file.read()
        
    # Send the bytes to our new service
    text = extract_text_from_pdf(raw_bytes)
    
    print("\n--- EXTRACTION SUCCESSFUL ---\n")
    print(text[:500]) # Print just the first 500 characters so we don't flood the terminal
    print("\n-----------------------------\n")
    print(f"Total characters extracted: {len(text)}")
    
except FileNotFoundError:
    print(f"❌ Error: Could not find {file_path}. Make sure you dragged a PDF into the folder!")
except Exception as e:
    print(f"❌ Error: {str(e)}")