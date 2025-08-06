# Use the official Python image.
FROM python:3.9-slim

RUN wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O /app/global-bundle.pem
# Set the working directory.
WORKDIR /app

# Copy the current directory contents into the container.
COPY . /app

# Install dependencies.
RUN pip install -r requirements.txt

EXPOSE 8080

# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]