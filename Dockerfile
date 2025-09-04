FROM python:3.13 AS base

RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app/src

COPY src/ /app/src/


CMD ["fastapi", "run", "--workers", "4", "app/main.py"]