"""
Calcul des métriques d'évaluation des modèles de prédiction.
Métriques implémentées : R², RMSE, MAPE, Accuracy ±10%, temps d'inférence.
"""

import time
import logging
from typing import Any
import numpy as np
import pandas as pd

# pylint: disable=invalid-name

logger = logging.getLogger(__name__)


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Coefficient de détermination R² (coefficient de détermination).
    R² = 1 - SS_res / SS_tot

    R² = 1 → prédiction parfaite
    R² = 0 → modèle équivalent à la moyenne
    R² < 0 → modèle pire que la moyenne
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Root Mean Square Error (MW).
    RMSE = √(1/n · Σ(yᵢ - ŷᵢ)²)

    Pénalise fortement les grandes erreurs.
    """
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mape(y_true: np.ndarray, y_pred: np.ndarray,
         epsilon: float = 1e-8) -> float:
    """
    Mean Absolute Percentage Error (%).
    MAPE = (100/n) · Σ|yᵢ - ŷᵢ| / |yᵢ|

    Métrique principale chez EDF pour évaluer la précision des prévisions.
    Cible : MAPE ≤ 4 %.
    """
    return float(np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + epsilon))) * 100)


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error (MW)."""
    return float(np.mean(np.abs(y_true - y_pred)))


def accuracy_within_tolerance(y_true: np.ndarray, y_pred: np.ndarray,
                                tolerance: float = 0.10) -> float:
    """
    Taux de prédictions dans la plage ±tolerance de la valeur réelle (%).
    Exemple : tolerance=0.10 → prédiction acceptable si |erreur| ≤ 10 %.
    """
    relative_error = np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))
    return float(np.mean(relative_error <= tolerance) * 100)


def inference_time_ms(model: Any, X_sample: np.ndarray,
                       n_repeat: int = 100) -> float:
    """
    Mesure le temps d'inférence moyen (ms) pour une seule prédiction.
    Utile pour valider le SLA de l'API (< 500 ms par requête).
    """
    _ = model.predict(X_sample[:1])  # warmup

    start = time.perf_counter()
    for _ in range(n_repeat):
        model.predict(X_sample[:1])
    end = time.perf_counter()

    return float((end - start) / n_repeat * 1000)


def evaluate_model(model: Any, X_test: np.ndarray, y_test: np.ndarray,
                   model_name: str = "Modèle") -> dict:
    """
    Évalue un modèle sur toutes les métriques et affiche un rapport.

    Args:
        model      : Modèle scikit-learn entraîné (doit avoir .predict())
        X_test     : Features de test normalisées
        y_test     : Valeurs cibles de test
        model_name : Nom du modèle pour l'affichage

    Returns:
        dict contenant toutes les métriques
    """
    y_pred = model.predict(X_test)

    metrics = {
        "model_name": model_name,
        "r2": round(r2_score(y_test, y_pred), 4),
        "rmse_mw": round(rmse(y_test, y_pred), 1),
        "mape_pct": round(mape(y_test, y_pred), 2),
        "mae_mw": round(mae(y_test, y_pred), 1),
        "accuracy_10pct": round(accuracy_within_tolerance(y_test, y_pred, 0.10), 1),
        "accuracy_5pct": round(accuracy_within_tolerance(y_test, y_pred, 0.05), 1),
        "inference_ms": round(inference_time_ms(model, X_test), 2),
        "n_test_samples": len(y_test),
    }

    # ── Rapport formaté ──
    sep = "─" * 55
    print(f"\n{sep}")
    print(f"  ÉVALUATION — {model_name}")
    print(sep)
    print(f"  R² Score          : {metrics['r2']:.4f}  (cible ≥ 0.90)")
    print(f"  RMSE              : {metrics['rmse_mw']:,.0f} MW")
    print(f"  MAPE              : {metrics['mape_pct']:.2f} %  (cible ≤ 4 %)")
    print(f"  MAE               : {metrics['mae_mw']:,.0f} MW")
    print(f"  Accuracy ±10 %    : {metrics['accuracy_10pct']:.1f} %")
    print(f"  Accuracy ±5 %     : {metrics['accuracy_5pct']:.1f} %")
    print(f"  Tps inférence     : {metrics['inference_ms']:.1f} ms  (cible < 500 ms)")
    print(f"  Échantillons test : {metrics['n_test_samples']}")
    print(sep)

    # Évaluation des objectifs EDF
    _check_objectives(metrics)

    logger.info(
        "[%s] R²=%.3f MAPE=%.2f%%",
        model_name,
        metrics["r2"],
        metrics["mape_pct"],
    )
    return metrics


def _check_objectives(metrics: dict) -> None:
    """Affiche un bilan vert/rouge des objectifs EDF."""
    checks = [
        ("R² ≥ 0.90", metrics["r2"] >= 0.90),
        ("MAPE ≤ 4 %", metrics["mape_pct"] <= 4.0),
        ("Accuracy ±10 % ≥ 90 %", metrics["accuracy_10pct"] >= 90.0),
        ("Inférence < 500 ms", metrics["inference_ms"] < 500),
    ]
    print("\n  Objectifs EDF :")
    for label, passed in checks:
        status = "Ok" if passed else "Ko"
        print(f"    {status}  {label}")


def compare_models(results: dict):
    """
    Affiche un tableau comparatif des modèles et retourne un DataFrame.

    Args:
        results : dict {nom_modele: metrics_dict} retournés par evaluate_model()

    Returns:
        pd.DataFrame trié par R² décroissant
    """


    rows = list(results.values())
    df = pd.DataFrame(rows).sort_values("r2", ascending=False).reset_index(drop=True)

    print("\n" + "═" * 80)
    print("  COMPARAISON DES MODÈLES")
    print("═" * 80)
    header = f"{'Modèle':<28} {'R²':>6} {'RMSE (MW)':>10} {'MAPE %':>8} {'Acc±10%':>8} {'ms':>6}"
    print(header)
    print("─" * 80)

    best_r2 = df["r2"].max()
    for _, row in df.iterrows():
        marker = " ◄ MEILLEUR" if row["r2"] == best_r2 else ""
        line = (
            f"  {row['model_name']:<26} "
            f"{row['r2']:>6.4f} "
            f"{row['rmse_mw']:>10,.0f} "
            f"{row['mape_pct']:>8.2f} "
            f"{row['accuracy_10pct']:>8.1f} "
            f"{row['inference_ms']:>6.1f}"
            f"{marker}"
        )
        print(line)

    print("═" * 80)
    print(f"\n  → Recommandation production : {df.iloc[0]['model_name']}")
    return df
