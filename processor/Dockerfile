# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python dependencies file to the container
COPY requirements.txt /app/

# Install OS packages dependencies for better handling of python packages during build
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container (except what's excluded in .dockerignore)
COPY . /app

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Command to run on container start
CMD ["python3", "app.py"]
