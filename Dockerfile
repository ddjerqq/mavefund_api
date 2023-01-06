FROM python:3.10-slim as build

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

EXPOSE 443

# Run application
CMD [ "python", "-m", "src"]