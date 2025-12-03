FROM python:3.10-slim

# Working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy project files
COPY . .

# Collect static files (safe even if DEBUG=True)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# === Tambahkan ENV Koyeb di sini ===
# Domain Koyeb kamu, TANPA https://
ENV KOYEB_APP_URL=${KOYEB_APP_URL}
ENV KOYEB_URL=${KOYEB_URL}
ENV SECRET_KEY=${SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}
ENV DEBUG=${DEBUG}

# Opsional: izinkan semua hosts
ENV DJANGO_ALLOWED_HOSTS=*

# Gunicorn command
CMD gunicorn web_kasir_GR.wsgi:application --bind 0.0.0.0:$PORT



