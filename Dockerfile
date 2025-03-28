# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI application
COPY . .

# Expose the application port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



## Use an official Python runtime as a parent image
#FROM python:3.9-slim
#
## Set the working directory inside the container
#WORKDIR /fastapi_project
#
## Copy the current directory contents into the container at /fastapi_project
#COPY . /fastapi_project/
#
## Install dependencies
#RUN apt-get update && apt-get install -y \
#    build-essential \
#    libpq-dev \
#    && rm -rf /var/lib/apt/lists/* \
#    && pip install --no-cache-dir -r requirements.txt
#
## Expose port 8000 to allow access to the FastAPI application
#EXPOSE 8000
#
## Run the FastAPI application using Uvicorn
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#
##COPY wait-for-it.sh /wait-for-it.sh
##RUN chmod +x /wait-for-it.sh
