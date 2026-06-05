"""
API REST — Prédiction de la Consommation Électrique EDF
FastAPI + JWT + Prometheus metrics
"""
import os
import time
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from api.schemas import (
    PredictionRequest, PredictionResponse,
    HealthResponse, ModelMetricsResponse
)
from api.auth import create_access_token, get_current_user, require_role
from data_pipeline.preprocessing import build_features, get_feature_columns
from models.rbf_network import RBFNetwork

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Chemins ──
MODELS_PATH    = Path(os.getenv("MODELS_PATH", "data/models_saved"))
PROCESSED_PATH = Path(os.getenv("PROCESSED_PATH", "data/processed"))

# ── Prometheus metrics ──
PREDICTION_COUNTER  = Counter("edf_predictions_total", "Nombre de prédictions", ["model", "status"])
PREDICTION_LATENCY  = Histogram("edf_prediction_latency_seconds", "Latence prédiction", ["model"])
MAPE_GAUGE          = Gauge("edf_model_mape_pct", "MAPE du modèle", ["model"])
MODELS_LOADED_GAUGE = Gauge("edf_models_loaded", "Nombre de modèles chargés")

# ── State global ──
state = {
    "models": {},
    "scaler": None,
    "feature_cols": None,
    "start_time": time.time(),
    "model_metrics": {}
}

MODEL_FILES = {
    "random_forest":  "random_forest_v1.pkl",
    "decision_tree":  "decision_tree_v1.pkl",
    "rbf_network":    "rbf_network_v1.pkl",
    "knn":            "knn_v1.pkl",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──
    logger.info("Chargement des modèles ML...")
    for model_key, filename in MODEL_FILES.items():
        path = MODELS_PATH / filename
        if path.exists():
            try:
                if model_key == "rbf_network":
                    state["models"][model_key] = RBFNetwork.load(str(path))
                else:
                    state["models"][model_key] = joblib.load(path)
                logger.info(f" {model_key} chargé")
            except Exception as e:
                logger.warning(f"  {model_key} non chargé : {e}")
        else:
            logger.warning(f"  Fichier modèle absent : {path}")

    scaler_path = PROCESSED_PATH / "scaler.pkl"
    if scaler_path.exists():
        state["scaler"] = joblib.load(scaler_path)
        logger.info(" Scaler chargé")

    fc_path = PROCESSED_PATH / "feature_cols.csv"
    if fc_path.exists():
        state["feature_cols"] = pd.read_csv(fc_path, header=None)[0].tolist()
        logger.info(f" {len(state['feature_cols'])} features chargées")

    MODELS_LOADED_GAUGE.set(len(state["models"]))
    logger.info(f"API prête — {len(state['models'])} modèles disponibles")
    yield
    # ── Shutdown ──
    logger.info("Arrêt de l'API")


app = FastAPI(
    title="EDF Consommation Électrique API",
    description="API de prédiction de la consommation électrique nationale — Projet MSPR EDF",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _build_feature_vector(req: PredictionRequest) -> np.ndarray:
    """Construit le vecteur de features normalisé à partir de la requête."""
    d = pd.Timestamp(req.date)
    row = {
        "date":               d,
        "consommation_mw":    0,  # placeholder (non utilisé en prédiction)
        "temperature_moyenne": req.temperature_moyenne,
        "temperature_min":    req.temperature_min,
        "temperature_max":    req.temperature_max,
        "type_jour":          req.type_jour,
        "mois":               d.month,
        "jour_semaine":       d.dayofweek,
        "consommation_j1":    0,
        "consommation_j7":    0,
        "consommation_j14":   0,
        "consommation_ma7":   0,
    }
    df_row = pd.DataFrame([row])
    df_feat = build_features(df_row)

    feature_cols = state["feature_cols"] or get_feature_columns()
    X = df_feat[feature_cols].values

    if state["scaler"] is not None:
        X = state["scaler"].transform(X)

    return X


# ── Routes ──

@app.get("/", tags=["Info"])
def root():
    return {"service": "EDF Prediction API", "version": "1.0.0", "status": "running"}


@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
def health():
    return HealthResponse(
        status="healthy" if state["models"] else "degraded",
        models_loaded={k: True for k in state["models"]},
        version="1.0.0",
        uptime_seconds=round(time.time() - state["start_time"], 1)
    )


@app.get("/metrics", tags=["Monitoring"])
def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/auth/token", tags=["Auth"])
def get_token(username: str, password: str):
    """Endpoint de démonstration — remplacer par LDAP EDF en production."""
    users = {
        "operateur_edf": ("edf2025!", "reader"),
        "analyste":      ("analyse2025!", "analyst"),
        "admin":         ("admin2025!", "admin"),
    }
    if username not in users or users[username][0] != password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    role = users[username][1]
    token = create_access_token(subject=username, role=role)
    return {"access_token": token, "token_type": "bearer", "role": role}


@app.post("/predict", response_model=PredictionResponse, tags=["Prédiction"])
def predict(
    req: PredictionRequest,
    user: dict = Depends(get_current_user)
):
    model_key = req.model
    if model_key not in state["models"]:
        available = list(state["models"].keys())
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Modèle '{model_key}' non disponible. Disponibles : {available}"
        )

    model = state["models"][model_key]

    try:
        t0 = time.time()
        X = _build_feature_vector(req)
        y_pred = float(model.predict(X)[0])
        latency = (time.time() - t0) * 1000

        PREDICTION_COUNTER.labels(model=model_key, status="success").inc()
        PREDICTION_LATENCY.labels(model=model_key).observe(latency / 1000)

        logger.info(f"Prédiction {req.date} | {model_key} | {y_pred:,.0f} MW | {latency:.1f}ms")

        return PredictionResponse(
            date=str(req.date),
            consommation_predite_mw=round(y_pred, 0),
            consommation_predite_gw=round(y_pred / 1000, 3),
            model_used=model_key,
            confidence_interval_low_mw=round(y_pred * 0.90, 0),
            confidence_interval_high_mw=round(y_pred * 1.10, 0),
            inference_time_ms=round(latency, 2)
        )

    except Exception as e:
        PREDICTION_COUNTER.labels(model=model_key, status="error").inc()
        logger.error(f"Erreur prédiction : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")


@app.get("/models", tags=["Modèles"])
def list_models(user: dict = Depends(get_current_user)):
    return {
        "available_models": list(state["models"].keys()),
        "default": "random_forest",
        "recommended_for_production": "random_forest"
    }


@app.get("/models/{model_name}/metrics", response_model=ModelMetricsResponse, tags=["Modèles"])
def get_model_metrics(
    model_name: str,
    user: dict = Depends(require_role("analyst"))
):
    import json
    metrics_files = {
        "random_forest": "metrics_random_forest.json",
        "decision_tree": "metrics_decision_tree.json",
        "rbf_network":   "metrics_rbf_network.json",
        "knn":           "metrics_knn.json",
    }
    if model_name not in metrics_files:
        raise HTTPException(status_code=404, detail=f"Modèle '{model_name}' inconnu")

    path = MODELS_PATH / metrics_files[model_name]
    if not path.exists():
        raise HTTPException(status_code=404, detail="Métriques non disponibles")

    with open(path, encoding="utf-8") as f:
        metrics = json.load(f)

    return ModelMetricsResponse(
        model_name=model_name,
        r2=metrics.get("r2", 0.0),
        rmse_mw=metrics.get("rmse_mw", 0.0),
        mape_pct=metrics.get("mape_pct", 0.0),
        accuracy_10pct=metrics.get("accuracy_10pct", 0.0),
        inference_ms=metrics.get("inference_ms", 0.0),
        training_date=metrics.get("training_date", "N/A")
    )
