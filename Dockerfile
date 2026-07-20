# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY bot.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port - Railway will set this dynamically
EXPOSE 5000

# Run the application with gunicorn using environment variable
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} bot:app
