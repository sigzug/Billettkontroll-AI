FROM python:3.10-slim-buster

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install the required Python libraries
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . /app

EXPOSE 8080

# Set the environment variable for Gunicorn
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --workers=4"

ENTRYPOINT ["gunicorn"]
CMD ["main:app"]