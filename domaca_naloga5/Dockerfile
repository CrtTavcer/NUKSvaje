# FastAPI
# Use an official Python runtime as a parent image
FROM python:3.10.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

COPY *.py ./
COPY __pycache__ .
COPY Avtodatabase.db .

# Expose port 80 to the outside world
EXPOSE 8000

# Define the command to run the application when the container starts
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]