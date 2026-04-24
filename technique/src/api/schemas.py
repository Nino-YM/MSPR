from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import date


class PredictionRequest(BaseModel):
    date: date = Field(..., description="Date de prédiction (YYYY-MM-DD)")
    temperature_moyenne: float = Field(..., ge=-20, le=45, description="Température moyenne en °C")
    temperature_min: float = Field(..., ge=-25, le=40, description="Température minimale en °C")
    temperature_max: float = Field(..., ge=-15, le=50, description="Température maximale en °C")
    type_jour: Literal[0, 1, 2] = Field(..., description="0=Ouvré, 1=Week-end, 2=Férié")
    model: Literal["random_forest", "decision_tree", "rbf_network", "knn"] = Field(
        default="random_forest",
        description="Modèle à utiliser pour la prédiction"
    )

    @field_validator("temperature_min")
    @classmethod
    def temp_min_lt_max(cls, v, info):
        if "temperature_max" in info.data and v >= info.data["temperature_max"]:
            raise ValueError("temperature_min doit être inférieure à temperature_max")
        return v

    model_config = {"json_schema_extra": {
        "example": {
            "date": "2025-01-15",
            "temperature_moyenne": 5.0,
            "temperature_min": 1.0,
            "temperature_max": 9.0,
            "type_jour": 0,
            "model": "random_forest"
        }
    }}


class PredictionResponse(BaseModel):
    date: str
    consommation_predite_mw: float = Field(..., description="Consommation prédite en MW")
    consommation_predite_gw: float = Field(..., description="Consommation prédite en GW")
    model_used: str
    confidence_interval_low_mw: float = Field(..., description="Borne basse intervalle ±10%")
    confidence_interval_high_mw: float = Field(..., description="Borne haute intervalle ±10%")
    inference_time_ms: float


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    models_loaded: dict[str, bool]
    version: str
    uptime_seconds: float


class ModelMetricsResponse(BaseModel):
    model_name: str
    r2: float
    rmse_mw: float
    mape_pct: float
    accuracy_10pct: float
    inference_ms: float
    training_date: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: str
