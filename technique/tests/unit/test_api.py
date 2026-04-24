"""
Tests unitaires — API FastAPI
pytest tests/unit/test_api.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from fastapi.testclient import TestClient

from api.auth import create_access_token, decode_token
from api.schemas import PredictionRequest, PredictionResponse


# ── Tests Auth ────────────────────────────────────────────────────────────────

class TestAuth:

    def test_create_and_decode_token(self):
        token = create_access_token("test_user", role="analyst")
        payload = decode_token(token)
        assert payload["sub"] == "test_user"
        assert payload["role"] == "analyst"

    def test_token_contains_expiry(self):
        token = create_access_token("user")
        payload = decode_token(token)
        assert "exp" in payload
        assert "iat" in payload

    def test_invalid_token_raises(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            decode_token("invalid.token.here")
        assert exc_info.value.status_code == 401

    def test_reader_role_default(self):
        token = create_access_token("user")
        payload = decode_token(token)
        assert payload["role"] == "reader"


# ── Tests Schemas ─────────────────────────────────────────────────────────────

class TestSchemas:

    def test_valid_request(self):
        req = PredictionRequest(
            date="2025-01-15",
            temperature_moyenne=5.0,
            temperature_min=1.0,
            temperature_max=9.0,
            type_jour=0
        )
        assert req.model == "random_forest"  # Défaut

    def test_temperature_range_validation(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            PredictionRequest(
                date="2025-01-15",
                temperature_moyenne=60.0,  # > 45°C
                temperature_min=1.0,
                temperature_max=9.0,
                type_jour=0
            )

    def test_invalid_type_jour(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            PredictionRequest(
                date="2025-01-15",
                temperature_moyenne=5.0,
                temperature_min=1.0,
                temperature_max=9.0,
                type_jour=5  # Doit être 0, 1 ou 2
            )

    def test_invalid_model_name(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            PredictionRequest(
                date="2025-01-15",
                temperature_moyenne=5.0,
                temperature_min=1.0,
                temperature_max=9.0,
                type_jour=0,
                model="xgboost"  # Modèle non supporté
            )


# ── Tests API Endpoints (avec mocks) ─────────────────────────────────────────

class TestAPIEndpoints:
    """
    Tests des endpoints API avec mocks des modèles ML.
    Les modèles ne sont pas chargés pour ne pas dépendre des fichiers .pkl.
    """

    @pytest.fixture(autouse=True)
    def setup_mock_state(self):
        """Configure un état simulé de l'API avec un modèle mock."""
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([65000.0])  # 65 GW

        from api import main
        original_state = main.state.copy()
        main.state["models"] = {"random_forest": mock_model}
        main.state["scaler"] = None
        main.state["feature_cols"] = [
            "consommation_j1", "consommation_j7", "consommation_j14",
            "consommation_ma7", "temperature_moyenne", "temperature_min",
            "temperature_max", "mois_sin", "mois_cos", "jour_sin", "jour_cos",
            "est_ouvre", "est_weekend", "est_hiver"
        ]
        main.state["start_time"] = 0.0

        yield

        main.state.update(original_state)

    @pytest.fixture
    def client(self):
        from api.main import app
        return TestClient(app, raise_server_exceptions=False)

    @pytest.fixture
    def auth_headers(self):
        token = create_access_token("test_user", role="analyst")
        return {"Authorization": f"Bearer {token}"}

    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "models_loaded" in data

    def test_predict_without_auth_returns_403(self, client):
        payload = {
            "date": "2025-01-15",
            "temperature_moyenne": 5.0,
            "temperature_min": 1.0,
            "temperature_max": 9.0,
            "type_jour": 0
        }
        response = client.post("/predict", json=payload)
        assert response.status_code in [401, 403]

    def test_predict_with_auth_returns_200(self, client, auth_headers):
        payload = {
            "date": "2025-01-15",
            "temperature_moyenne": 5.0,
            "temperature_min": 1.0,
            "temperature_max": 9.0,
            "type_jour": 0,
            "model": "random_forest"
        }
        response = client.post("/predict", json=payload, headers=auth_headers)
        assert response.status_code == 200

    def test_predict_response_structure(self, client, auth_headers):
        payload = {
            "date": "2025-06-15",
            "temperature_moyenne": 20.0,
            "temperature_min": 15.0,
            "temperature_max": 28.0,
            "type_jour": 1,
            "model": "random_forest"
        }
        response = client.post("/predict", json=payload, headers=auth_headers)
        if response.status_code == 200:
            data = response.json()
            assert "consommation_predite_mw" in data
            assert "consommation_predite_gw" in data
            assert "confidence_interval_low_mw" in data
            assert "confidence_interval_high_mw" in data
            assert data["confidence_interval_low_mw"] < data["consommation_predite_mw"]
            assert data["confidence_interval_high_mw"] > data["consommation_predite_mw"]

    def test_predict_unavailable_model(self, client, auth_headers):
        payload = {
            "date": "2025-01-15",
            "temperature_moyenne": 5.0,
            "temperature_min": 1.0,
            "temperature_max": 9.0,
            "type_jour": 0,
            "model": "knn"  # Non chargé dans le mock
        }
        response = client.post("/predict", json=payload, headers=auth_headers)
        assert response.status_code == 503

    def test_list_models_endpoint(self, client, auth_headers):
        response = client.get("/models", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "available_models" in data
        assert "random_forest" in data["available_models"]
