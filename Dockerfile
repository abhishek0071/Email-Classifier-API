# ── 1. base image ───────────────────────────────────────────────
FROM python:3.12-slim

# ── 2. system packages (compile wheels for uvicorn[standard]) ──
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# ── 3. set workdir & install deps ───────────────────────────────
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── 4. copy application code ───────────────────────────────────
COPY app ./app

# ── 5. runtime command (prod) ──────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
