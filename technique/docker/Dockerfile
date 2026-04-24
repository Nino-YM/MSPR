# ── Stage 1 : Build ──────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ── Stage 2 : Production ─────────────────────────────────────────────────────
FROM python:3.10-slim AS production

# Métadonnées image
LABEL maintainer="edf-ia-team@edf.fr"
LABEL version="1.0.0"
LABEL description="API de prédiction de la consommation électrique EDF"

# Sécurité : utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copier les dépendances depuis le stage builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code source
COPY src/ ./src/
COPY data/models_saved/ ./data/models_saved/
COPY data/processed/scaler.pkl ./data/processed/scaler.pkl
COPY data/processed/feature_cols.csv ./data/processed/feature_cols.csv

# Variables d'environnement
ENV PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODELS_PATH=/app/data/models_saved \
    PROCESSED_PATH=/app/data/processed \
    JWT_SECRET_KEY=change-me-in-production

# Permissions
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "2", "--access-log", "--log-level", "info"]
