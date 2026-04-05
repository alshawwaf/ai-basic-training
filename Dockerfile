FROM python:3.11-slim

# System deps for matplotlib rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages (heaviest first for layer caching)
COPY portal/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (portal + all stage exercise files)
COPY . /app

WORKDIR /app/portal

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

CMD ["python", "app.py"]
