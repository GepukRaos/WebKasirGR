FROM python:3.10-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy project
COPY . .

# (IMPORTANT) DO NOT run collectstatic or migrate at build time
# They MUST run at runtime, when environment variables exist.

# Expose port (optional)
EXPOSE 8000

# Start gunicorn with KOYEB-$PORT
CMD gunicorn web_kasir_GR.wsgi:application --bind 0.0.0.0:$PORT
