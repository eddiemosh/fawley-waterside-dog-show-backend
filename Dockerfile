# Use the official Python image.
FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Download global bundle (AFTER WORKDIR is set, so it saves to correct place)
RUN apt-get update && apt-get install -y wget && \
    wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O /app/global-bundle.pem && \
    apt-get remove -y wget && apt-get autoremove -y && apt-get clean

# Copy the current directory contents into the container.
COPY . /app

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
