FROM python:3.11-slim as build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev

# Install Python dependencies \
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Path: Dockerfile
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev

# Copy Python dependencies \
COPY --from=build /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . /app
WORKDIR /app

# Run application
CMD ["python", "-3.11", "app"]