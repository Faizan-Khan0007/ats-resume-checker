# 1. Start with a lightweight version of Python 3.11
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (makes building faster)
COPY requirements.txt .

# 4. Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your backend files into the container
COPY . .

# 6. Expose port 8000 so we can talk to it
EXPOSE 8000

# 7. The command to start your FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]