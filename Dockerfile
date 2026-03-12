FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

EXPOSE 8000

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI (safe method)
RUN pip install awscli

CMD ["python3","app.py"]