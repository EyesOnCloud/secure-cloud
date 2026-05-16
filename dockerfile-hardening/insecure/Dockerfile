# ─────────────────────────────────────────────────────────────────────────────
# INSECURE DOCKERFILE
# This Dockerfile contains deliberate security misconfigurations.
# Participants identify and fix each one.
# DO NOT use this pattern in production.
# ─────────────────────────────────────────────────────────────────────────────

# ISSUE 1: Unpinned, bloated base image
# ubuntu:latest is ~70MB compressed and carries hundreds of packages
# that have nothing to do with running a Python application.
# "latest" is a mutable tag — tomorrow's latest may be different from today's.
FROM ubuntu:latest

# ISSUE 2: No package cache cleanup after apt install
# The apt cache (lists, archives) is retained in the layer permanently.
# Every subsequent image pull carries this unnecessary data.
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    gcc \
    curl \
    wget \
    net-tools \
    iputils-ping \
    vim \
    git \
    openssh-client \
    sudo

# ISSUE 3: Hardcoded secret in environment variable
# This value is baked into the image layer permanently.
# Removing it in a later layer does NOT remove it from the image history.
# Anyone with docker history --no-trunc can read this value.
ENV API_KEY=prod-api-key-DO-NOT-COMMIT-abc123xyz
ENV DATABASE_URL=postgresql://admin:SuperSecretProdPassword@db.internal:5432/payments
ENV FLASK_ENV=development
ENV DEBUG=true

# ISSUE 4: Copying everything including sensitive files
# .git directory, local .env files, test files, credentials —
# whatever is in the build context gets copied into the image.
WORKDIR /app
COPY . .

# ISSUE 5: Installing dependencies as root with no version pinning
# pip install without --no-cache-dir bloats the image with pip's cache.
# No version pinning means non-deterministic builds.
RUN pip3 install flask requests boto3 psycopg2-binary

# ISSUE 6: Running as root (no USER instruction)
# The absence of a USER instruction means the process runs as UID 0.
# Root inside a container has broad capabilities and can
# escape to the host under certain Docker configurations.

# ISSUE 7: Exposing a debugging port and using EXPOSE with no restriction
EXPOSE 8080
EXPOSE 5678

# ISSUE 8: No health check defined
# Without a HEALTHCHECK, the container orchestrator cannot detect
# when the application inside has crashed or is unresponsive.

CMD ["python3", "app.py"]
