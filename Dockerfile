# Use the official Python image.
FROM python:3.11-slim

# Set the working directory.
WORKDIR /app

# Copy the current directory contents into the container.
COPY . /app

# Install dependencies.
RUN pip install fastapi uvicorn

# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]