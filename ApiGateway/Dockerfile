FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .
COPY main.py .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app into the container
COPY . .

# Expose port 8000
EXPOSE 5003

CMD ["python3", "main.py"]