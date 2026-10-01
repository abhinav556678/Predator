# =========================================================================
# PREDATOR Deception Subsystem - Hardened Dockerfile
# Ticket 02 & Ticket 11: Deception Environment Setup & Isolation
# =========================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DECEPTION_HOST=0.0.0.0
ENV DECEPTION_PORT=8080
ENV DECEPTION_SECONDARY_PORT=9000
ENV M3_BACKEND_URL=http://host.docker.internal:8000/events

WORKDIR /app

# Install minimal OS dependencies and security tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install required Python dependencies
COPY deception/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create an unprivileged user for security isolation (no host breakout)
RUN groupadd -g 10001 deception_group && \
    useradd -u 10001 -g deception_group -s /bin/bash -m deception_user

# Copy application files
COPY deception /app/deception

# Create isolated data and logs directories with correct permissions
RUN mkdir -p /app/deception/logs /app/deception/fake_database && \
    chown -R deception_user:deception_group /app

# Switch to unprivileged user
USER deception_user

# Pre-seed the fake corporate database
RUN python -m deception.fake_database.fake_db

# Expose primary and secondary deception ports
EXPOSE 8080 9000

# Docker Healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8080/health || exit 1

# Launch the Deception server
CMD ["python", "deception/run_deception.py", "--host", "0.0.0.0", "--port", "8080"]
