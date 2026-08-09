# syntax=docker/dockerfile:1

# ---------- builder ----------
FROM python:3.14-slim AS builder

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
FROM python:3.14-slim AS runtime

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

# Numeric, not `USER app`. With runAsNonRoot the kubelet must confirm the image's
# user is not root, and it cannot resolve a name — only a UID. A named user fails
# with "cannot verify user is non-root" unless the pod also sets runAsUser.
USER 1000:1000

EXPOSE 5000

# CMD, not ENTRYPOINT: single-purpose image, so `docker run img sh` should just work.
# Use ENTRYPOINT when the binary is fixed and only its args should change.
# In k8s: ENTRYPOINT = pod `command:`, CMD = pod `args:`.
# Exec form (JSON array) is required — shell form makes /bin/sh PID 1, which
# swallows SIGTERM and blocks graceful shutdown.
#
# --worker-tmp-dir /dev/shm keeps gunicorn's heartbeat files off the read-only rootfs.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "run:app"]
