# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV (optional, but if you want to use uv inside container)
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
# OR just install requirements with pip for simplicity in container if requirements.txt exists
# For now, we'll assume standard pip install from generated requirements or similar
# But since we are using uv locally, we should export requirements.

# Copy project
COPY . /app/

# Install python dependencies
# We will use a trick: check if uv.lock exists, if so use it, else install from pyproject.toml
# For simplicity in this phase, let's assume we install 'uv' and use it to sync.
RUN pip install uv
RUN uv sync --frozen || uv sync

# Expose port
EXPOSE 8000

