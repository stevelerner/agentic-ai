# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ ./agents/
COPY tools/ ./tools/
COPY memory/ ./memory/
COPY api/ ./api/
COPY examples/ ./examples/
COPY cli.py .

# Create non-root user
RUN useradd -m -u 1000 agent && \
    chown -R agent:agent /app && \
    mkdir -p /app/outputs && \
    chown -R agent:agent /app/outputs

USER agent

# Default command (can be overridden)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

