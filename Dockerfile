# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /financial_app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /financial_app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY /financial_app /financial_app

RUN cd financial_app
# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "financial_app.wsgi:application", "--bind", "0.0.0.0:8000"]
