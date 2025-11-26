FROM python:3.10-slim

# Working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (safe even if DEBUG=True)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Gunicorn command
CMD ["gunicorn", "web_kasir_GR.wsgi:application", "--bind", "0.0.0.0:8000"]
