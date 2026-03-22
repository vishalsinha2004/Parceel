# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (GDAL and PostGIS)
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin python3-gdal postgis \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 10000

# Run the ASGI server using uvicorn (required for your Socket.IO implementation)
CMD gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}