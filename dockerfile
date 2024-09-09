# Use the official Python image from the Docker Hub as the base image
FROM python:3.11-slim

# Set environment variables to avoid Python buffering
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
# Specify the command to run your application
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]