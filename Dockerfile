FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI
RUN pip install --no-cache-dir awscli

# Copy project files
COPY . .

# Expose API port
EXPOSE 8000

CMD ["python","app.py"]

