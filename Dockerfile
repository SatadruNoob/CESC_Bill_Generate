# Use an official Ubuntu base image
FROM ubuntu:22.04

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender1 \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-osd \
    poppler-utils \
    wget \
    gnupg2 \
    python3 \
    python3-pip \
    python3-venv \
    # Install Google Chrome
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code into the Docker image
COPY . /app

# Create and activate a virtual environment, then install dependencies
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install -r requirements.txt

# Expose any necessary ports
EXPOSE 8000

# Command to run the application with increased Gunicorn timeout
CMD ["sh", "-c", ". venv/bin/activate && gunicorn -b :${PORT:-8000} --timeout 120 app:app"]
