FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (e.g., for building tools if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the HuggingFace model so it's cached in the image
# (You could also do this at runtime, but doing it in Docker build is faster for startup)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY ./app /app/app
COPY ./data /app/data

# Expose port
EXPOSE 8000

# Command to run the Fastapi app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
