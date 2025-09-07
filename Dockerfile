# ========================
# Base image (shared deps)
# ========================
FROM python:3.13 AS base

#Step 3: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH=/src

# ========================
# Development image
# ========================
FROM base AS dev
WORKDIR /src
COPY src/ /src
# Dev tools
RUN pip install --no-cache-dir uvicorn[standard]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ========================
# Production image
# ========================
FROM base AS prod
WORKDIR /src
COPY src/ /src
RUN pip install --no-cache-dir gunicorn uvicorn
# Multiple workers (Gunicorn + Uvicorn workers)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
