# Base image
FROM python:3.9-slim

# Working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run API
CMD ["uvicorn", "scripts.api:app", "--host", "0.0.0.0", "--port", "8010"]
