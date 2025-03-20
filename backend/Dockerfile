# Base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY backend/ /app/

# Expose the port for FastAPI
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "main:app", "--reload"]
