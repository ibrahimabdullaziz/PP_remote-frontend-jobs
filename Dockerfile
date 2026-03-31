FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set working directory
WORKDIR /app

# Copy requirement files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install browsers explicitly if needed
RUN playwright install chromium

# Copy the rest of the application
COPY . .

# Run the application
CMD ["python", "main.py"]
