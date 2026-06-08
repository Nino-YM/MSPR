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
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse, tags=["Info"])
def root():
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EDF — Prédiction de consommation</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: #f0f2f5;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08);
      padding: 2.5rem;
      width: 100%;
      max-width: 520px;
    }
    .logo { font-size: 2rem; font-weight: 800; color: #003189; margin-bottom: .25rem; }
    .subtitle { color: #666; font-size: .9rem; margin-bottom: 2rem; }
    .section-title {
      font-size: .7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: #999;
      margin: 1.5rem 0 .75rem;
    }
    .row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: .75rem; }
    .field { display: flex; flex-direction: column; gap: .35rem; margin-bottom: .75rem; }
    label { font-size: .85rem; font-weight: 500; color: #333; }
    input, select {
      padding: .55rem .75rem;
      border: 1.5px solid #e0e0e0;
      border-radius: 7px;
      font-size: .95rem;
      transition: border-color .15s;
      width: 100%;
    }
    input:focus, select:focus { outline: none; border-color: #003189; }
    .btn {
      width: 100%;
      padding: .85rem;
      background: #003189;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      margin-top: 1.5rem;
      transition: background .15s;
    }
    .btn:hover { background: #0042b8; }
    .btn:disabled { background: #a0aec0; cursor: not-allowed; }
    .result {
      margin-top: 1.5rem;
      padding: 1.25rem;
      border-radius: 8px;
      display: none;
    }
    .result.success { background: #f0f7ff; border: 1.5px solid #cce0ff; }
    .result.error   { background: #fff5f5; border: 1.5px solid #ffc5c5; }
    .result-title { font-weight: 700; font-size: 1rem; color: #003189; margin-bottom: .75rem; }
    .result.error .result-title { color: #c53030; }
    .result-row { display: flex; justify-content: space-between; font-size: .9rem; padding: .2rem 0; }
    .result-row span:last-child { font-weight: 600; }
    .result-main { font-size: 2rem; font-weight: 800; color: #003189; text-align: center; margin: .5rem 0; }
    .result-sub  { font-size: .85rem; color: #666; text-align: center; }
  </style>
</head>
<body>
<div class="card">
  <div class="logo">⚡ EDF</div>
  <div class="subtitle">Prédiction de consommation électrique nationale</div>

  <div class="section-title">Connexion</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
    <div class="field">
      <label for="username">Utilisateur</label>
      <input id="username" type="text" placeholder="operateur_edf" value="operateur_edf">
    </div>
    <div class="field">
      <label for="password">Mot de passe</label>
      <input id="password" type="password" placeholder="••••••••" value="edf2025!">
    </div>
  </div>

  <div class="section-title">Paramètres de prédiction</div>
  <div class="field">
    <label for="date">Date</label>
    <input id="date" type="date">
  </div>

  <div class="row">
    <div class="field">
      <label for="temp_moy">Temp. moy. (°C)</label>
      <input id="temp_moy" type="number" step="0.1" placeholder="5.0" value="5.0">
    </div>
    <div class="field">
      <label for="temp_min">Temp. min (°C)</label>
      <input id="temp_min" type="number" step="0.1" placeholder="1.0" value="1.0">
    </div>
    <div class="field">
      <label for="temp_max">Temp. max (°C)</label>
      <input id="temp_max" type="number" step="0.1" placeholder="9.0" value="9.0">
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
    <div class="field">
      <label for="type_jour">Type de jour</label>
      <select id="type_jour">
        <option value="0">Jour ouvré</option>
        <option value="1">Week-end</option>
        <option value="2">Jour férié</option>
      </select>
    </div>
    <div class="field">
      <label for="model">Modèle</label>
      <select id="model">
        <option value="random_forest">Random Forest</option>
        <option value="decision_tree">Decision Tree</option>
        <option value="rbf_network">RBF Network</option>
        <option value="knn">KNN</option>
      </select>
    </div>
  </div>

  <button class="btn" id="submit-btn" onclick="predict()">Lancer la prédiction</button>

  <div class="result" id="result">
    <div class="result-title" id="result-title"></div>
    <div class="result-main" id="result-main"></div>
    <div class="result-sub"  id="result-sub"></div>
    <div id="result-details"></div>
  </div>
</div>

<script>
  document.getElementById('date').valueAsDate = new Date();

  async function predict() {
    const btn = document.getElementById('submit-btn');
    const result = document.getElementById('result');
    btn.disabled = true;
    btn.textContent = 'Prédiction en cours…';
    result.style.display = 'none';

    try {
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      const authRes = await fetch('/auth/token?username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password), { method: 'POST' });
      if (!authRes.ok) { showError('Identifiants invalides'); return; }
      const { access_token } = await authRes.json();

      const body = {
        date:                 document.getElementById('date').value,
        temperature_moyenne:  parseFloat(document.getElementById('temp_moy').value),
        temperature_min:      parseFloat(document.getElementById('temp_min').value),
        temperature_max:      parseFloat(document.getElementById('temp_max').value),
        type_jour:            parseInt(document.getElementById('type_jour').value),
        model:                document.getElementById('model').value,
      };

      const predRes = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token },
        body: JSON.stringify(body),
      });

      if (!predRes.ok) {
        const err = await predRes.json();
        showError(err.detail || 'Erreur serveur');
        return;
      }

      const data = await predRes.json();
      showSuccess(data);

    } catch(e) {
      showError('Impossible de joindre le serveur');
    } finally {
      btn.disabled = false;
      btn.textContent = 'Lancer la prédiction';
    }
  }

  function showSuccess(data) {
    const r = document.getElementById('result');
    r.className = 'result success';
    document.getElementById('result-title').textContent = 'Résultat — ' + data.date;
    document.getElementById('result-main').textContent = (data.consommation_predite_gw).toFixed(2) + ' GW';
    document.getElementById('result-sub').textContent =
      'Intervalle de confiance : ' +
      (data.confidence_interval_low_mw/1000).toFixed(2) + ' – ' +
      (data.confidence_interval_high_mw/1000).toFixed(2) + ' GW';
    document.getElementById('result-details').innerHTML =
      '<div class="result-row"><span>Modèle</span><span>' + data.model_used + '</span></div>' +
      '<div class="result-row"><span>Valeur MW</span><span>' + data.consommation_predite_mw.toLocaleString('fr-FR') + ' MW</span></div>' +
      '<div class="result-row"><span>Temps d\'inférence</span><span>' + data.inference_time_ms.toFixed(2) + ' ms</span></div>';
    r.style.display = 'block';
  }

  function showError(msg) {
    const r = document.getElementById('result');
    r.className = 'result error';
    document.getElementById('result-title').textContent = 'Erreur';
    document.getElementById('result-main').textContent = '';
    document.getElementById('result-sub').textContent = '';
    document.getElementById('result-details').textContent = msg;
    r.style.display = 'block';
  }
</script>
</body>
</html>""")


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
