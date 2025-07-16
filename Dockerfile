FROM python:3.13.5-alpine

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/

# Expose port 8000 for metrics
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["python", "src/main.py"]
# Default command (can be overridden)
CMD ["--help"]
