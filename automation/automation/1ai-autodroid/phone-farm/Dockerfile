FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    adb \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r phonefarm && useradd -r -g phonefarm -d /app -s /sbin/nologin phonefarm

WORKDIR /app

COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; \
    else pip install --no-cache-dir fastapi uvicorn pillow; \
    fi

COPY *.py ./
COPY dashboard/ ./dashboard/
COPY static/ ./static/

RUN mkdir -p /app/logs/phone-farm && chown -R phonefarm:phonefarm /app

USER phonefarm

EXPOSE 8889

ENV PYTHONUNBUFFERED=1
ENV PHONEFARM_MODE=dashboard

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8889/health/live')" || exit 1

CMD ["python", "farm_daemon.py"]