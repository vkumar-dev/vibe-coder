# Vibe Coder - Docker Image
# For deployment on Railway, Render, Fly.io, etc.

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install gh -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p projects logs state

# Make scripts executable
RUN chmod +x *.sh *.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VIBE_INTERVAL=4

# Volume for persistent data
VOLUME ["/app/projects", "/app/logs", "/app/state"]

# Health check
HEALTHCHECK --interval=1h --timeout=5m --start-period=5m --retries=3 \
    CMD python -c "import os; os.path.exists('state/history.json')" || exit 1

# Run worker
CMD ["python", "run_worker.py"]
