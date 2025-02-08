FROM python:3.10-slim

WORKDIR /app

# Copy only requirements and setup files first
COPY requirements.txt setup.py README.md ./

# Install dependencies and package in editable mode
RUN pip install  -r requirements.txt && \
    pip install -e .

# Copy .env file
COPY .env .

# Copy source code
COPY src ./src

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8501

# Run the application
CMD ["python", "src/run.py"]