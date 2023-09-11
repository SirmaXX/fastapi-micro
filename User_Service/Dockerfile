FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .
COPY main.py .

# Upgrade pip and install packages from requirements.txt in a single RUN command
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app into the container
COPY . .

EXPOSE 5002

# Run the application using uvicorn
CMD ["python3", "main.py"]
