# AWS re:Invent 2025 Research Automation - Docker Image
# This Dockerfile creates a containerized environment for running the automation

FROM python:3.11-slim

# Install system dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY examples/ ./examples/
COPY config.yaml .
COPY run_automation.py .
COPY test_setup.py .

# Create output directories
RUN mkdir -p outputs/screenshots outputs/presentations outputs/data

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Make scripts executable
RUN chmod +x run_automation.py test_setup.py

# Set the entrypoint
ENTRYPOINT ["python", "run_automation.py"]

# Default command (can be overridden)
CMD ["--max-services", "10"]
