# Use the official Python base image
FROM python:3.13.0a4-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application code
COPY . .

# Copy the templates folder to the working directory
COPY templates /app/templates

# Copy the config.ini file to the working directory
#COPY config/config.ini .

# Expose the required port
EXPOSE 5000

# Set the environment variables (if needed)
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# Set the entry point
CMD ["python", "app.py"]
