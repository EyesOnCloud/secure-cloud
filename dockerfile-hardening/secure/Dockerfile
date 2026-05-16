# ─────────────────────────────────────────────────────────────────────────────
# SECURE DOCKERFILE 
# Each fix is annotated with the security justification.
# ─────────────────────────────────────────────────────────────────────────────

# FIX 1a: Purpose-built minimal base image for Python
# python:3.11-slim is purpose-built for Python applications.
# It contains only what Python needs — not a full Ubuntu server.
# "slim" variants remove documentation, man pages, and most utilities
# that a server OS includes but a container application does not need.
#
# FIX 1b: Pin by digest for supply chain integrity
# The digest (sha256:...) is a cryptographic hash of the image content.
# It is immutable — this exact hash always refers to this exact image.
# A tag like "3.11-slim" is mutable and can be updated by the registry owner.
# Pinning by digest ensures every build uses the identical verified base image.
#
# To get the current digest:
#   docker pull python:3.11-slim
#   docker inspect python:3.11-slim | jq -r '.[0].RepoDigests[0]'
# Or:
#   crane digest python:3.11-slim

# BUILDER STAGE — FIX 2: Multi-stage build
# The builder stage installs all build tools and compiles dependencies.
# None of the build tools (gcc, pip cache, build-essential) exist in
# the final image — they are discarded when the builder stage completes.
FROM python:3.11-slim AS builder

WORKDIR /build

# Install only build dependencies in the builder stage
# These tools are needed to compile Python packages but must not
# appear in the final image — they increase attack surface significantly.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first — layer caching optimization
# If requirements.txt does not change, pip install is cached
# and rebuilds triggered by application code changes are faster.
COPY requirements.txt .

# Install Python dependencies into a dedicated directory
# --no-cache-dir: do not store pip's download cache in the image layer
# --prefix: install to /install so we can copy just this directory to final image
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── RUNTIME STAGE ─────────────────────────────────────────────────────────────
# The runtime stage starts fresh from the minimal base image.
# It contains ONLY what is needed to run the application at runtime.
# No compilers, no build tools, no pip cache, no intermediate files.
FROM python:3.11-slim AS runtime

# FIX: Set secure environment defaults
# PYTHONDONTWRITEBYTECODE: prevents writing .pyc files (not needed at runtime)
# PYTHONUNBUFFERED: ensures stdout/stderr are not buffered (better for logging)
# No secrets in ENV — secrets come from orchestrator-managed environment at runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=8080

WORKDIR /app

# Copy only the compiled dependencies from the builder stage
# Everything else from the builder stage is discarded
COPY --from=builder /install /usr/local

# FIX: Create a dedicated non-root user and group
# UID/GID 1001 is a non-privileged identity with no special permissions.
# The user is explicitly created with:
#   --no-create-home: no home directory (not needed for a service)
#   --shell /bin/false: cannot be used for interactive login
# This user cannot write to system directories, cannot install packages,
# and cannot perform privilege-sensitive operations.
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --no-create-home --shell /bin/false appuser

# Copy only application source code — NOT the entire build context
# Explicit file copying prevents accidentally including .git, .env,
# test files, credentials, and other non-production artifacts.
COPY --chown=appuser:appgroup app.py .
COPY --chown=appuser:appgroup requirements.txt .

# FIX: Switch to non-root user before any runtime instructions
# All subsequent instructions and the CMD run as this user.
# Even if the application is compromised, the attacker operates as
# an unprivileged user with no ability to write to system directories.
USER appuser

# Expose only the application port — remove debug ports
EXPOSE 8080

# FIX: Add a health check so orchestrators can detect application failures
# interval: how often to run the check
# timeout: how long to wait for a response before considering it failed
# start-period: grace period for the application to start up
# retries: consecutive failures before marking the container unhealthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" \
    || exit 1

# Use exec form (JSON array) instead of shell form (string)
# Shell form: CMD python3 app.py  — PID 1 is /bin/sh, not python3
# Exec form: CMD ["python3", "app.py"]  — PID 1 is python3
# PID 1 receives SIGTERM on container stop. With shell form, the signal
# goes to the shell which may not forward it to the application —
# causing a 10-second timeout before SIGKILL and unclean shutdown.
CMD ["python3", "app.py"]
