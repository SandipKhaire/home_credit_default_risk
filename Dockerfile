# Use the official Python 3.13.1 slim image as the base
FROM python:3.13.1-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy the requirements file to the container
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py .

# Copy the trained model and shape file
COPY models /app/models
COPY src /app/src

EXPOSE 80
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "app:app"]

#http://localhost:8000/docs#/default/predict_predict_post


