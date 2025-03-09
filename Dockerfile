# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model directory
COPY model/ /app/model/

# Copy the API code
COPY api/ /app/api/

# Set Python path
ENV PYTHONPATH=/app

# Set environment variables
ENV MODEL_PATH=/app/model

# Expose the port the app runs on
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]