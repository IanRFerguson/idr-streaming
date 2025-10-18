FROM python:3.12-slim

WORKDIR /app

COPY devops/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/streaming /app/src
COPY src/data /app/src/data
COPY src/utilities /app/src/utilities