# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command to run Flask app
CMD ["python", "app.py"]
