# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary OS packages in one line to keep the image clean and compact
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependencies file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -v -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose port 5001 to the outside once the container has launched
EXPOSE 5001

# Define the command to run your app using Python 3
CMD ["python3", "app.py"]
