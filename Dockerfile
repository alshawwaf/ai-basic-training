FROM python:3.11-slim AS base

# System deps for matplotlib + compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages (heaviest first for layer caching)
COPY portal/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ── Production stage ─────────────────────────────────────────────────────────
FROM python:3.11-slim

# Copy only the Python environment (no gcc/g++ in final image)
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /usr/local/bin /usr/local/bin

# Create non-root user
RUN groupadd -r ninja && useradd -r -g ninja -d /app -s /usr/sbin/nologin ninja

WORKDIR /app

# Copy project files
COPY --chown=ninja:ninja . /app

# Temp directory for script execution (writable by ninja)
RUN mkdir -p /tmp/runner && chown ninja:ninja /tmp/runner

# Switch to non-root user
USER ninja

WORKDIR /app/portal

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg
ENV TMPDIR=/tmp/runner

# Gunicorn: 4 workers, 120s timeout (matches script execution limit)
CMD ["gunicorn", "app:app", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--timeout", "180", \
     "--max-requests", "500", \
     "--max-requests-jitter", "50", \
     "--access-logfile", "-"]
