FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask==3.0.3

COPY app.py .

EXPOSE 8080

LABEL org.opencontainers.image.title="image-signing-demo"
LABEL org.opencontainers.image.description="Demo app for Container Image Signing"
LABEL org.opencontainers.image.vendor="Security"

CMD ["python", "app.py"]
