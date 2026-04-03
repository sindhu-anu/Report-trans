FROM python:3.11-slim

# Install system dependencies (IMPORTANT for opencv + tesseract)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of code
COPY . .

# Run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]