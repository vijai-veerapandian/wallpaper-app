# syntax=docker/dockerfile:1

# ---------- builder ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dependencies land in their own venv so the runtime stage can take just this.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- runtime ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Fixed uid/gid so the Kubernetes securityContext can pin runAsUser: 1000.
RUN groupadd --system --gid 1000 app \
 && useradd  --system --uid 1000 --gid app --no-create-home app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

# Explicit copies, not `COPY . .` — the image gets the application and nothing else,
# independently of whether .dockerignore is correct.
COPY --chown=app:app app/    ./app/
COPY --chown=app:app config/ ./config/
COPY --chown=app:app run.py  ./

USER app

EXPOSE 5000

# --worker-tmp-dir /dev/shm keeps gunicorn's heartbeat files off the root filesystem,
# which the Deployment mounts read-only.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "run:app"]
