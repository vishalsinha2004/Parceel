# Use an official Python runtime
FROM python:3.12-slim

# Install system dependencies for GeoDjango (PostGIS/GDAL)
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    postgis \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files for Django Admin
RUN python manage.py collectstatic --noinput

# Start Uvicorn (ASGI) for WebSockets and Django
CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "10000"]