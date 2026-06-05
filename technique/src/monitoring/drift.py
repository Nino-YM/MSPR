"""
Détection de dérive du modèle en production (Data/Concept Drift).
Trois méthodes complémentaires :
  - KS Test  : dérive de la distribution des features (data drift)
  - PSI       : Population Stability Index (dérive de prédictions)
  - CUSUM     : détection de biais cumulatif sur les erreurs de prédiction
"""
import logging
import numpy as np
from scipy import stats
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class DriftReport:
    """Résultat d'une analyse de dérive."""
    drift_detected: bool
    method: str
    statistic: float
    threshold: float
    p_value: Optional[float] = None
    details: dict = field(default_factory=dict)
    recommendation: str = ""

    def __str__(self):
        status = " DÉRIVE DÉTECTÉE" if self.drift_detected else " Pas de dérive"
        return (
            f"[{self.method}] {status} | "
            f"stat={self.statistic:.4f} (seuil={self.threshold}) | "
            f"{self.recommendation}"
        )


def ks_test_drift(X_reference: np.ndarray, X_current: np.ndarray,
                  alpha: float = 0.05) -> DriftReport:
    """
    Test de Kolmogorov-Smirnov feature par feature.
    Détecte si la distribution des données d'entrée a changé.

    Déclenche une alerte si au moins 30 % des features présentent une dérive.
    """
    n_features = X_reference.shape[1]
    drifted_features = []
    max_stat = 0.0

    for i in range(n_features):
        stat, p_val = stats.ks_2samp(X_reference[:, i], X_current[:, i])
        if p_val < alpha:
            drifted_features.append(i)
        max_stat = max(max_stat, stat)

    drift_ratio = len(drifted_features) / n_features
    drift_detected = drift_ratio >= 0.30

    recommendation = (
        "Réentraîner le modèle avec les données récentes."
        if drift_detected else
        "Surveillance normale — pas d'action requise."
    )

    return DriftReport(
        drift_detected=drift_detected,
        method="KS Test",
        statistic=drift_ratio,
        threshold=0.30,
        details={
            "features_en_derive": drifted_features,
            "ratio_derive": round(drift_ratio, 3),
            "alpha": alpha,
        },
        recommendation=recommendation,
    )


def psi_drift(y_pred_reference: np.ndarray, y_pred_current: np.ndarray,
              n_bins: int = 10, threshold: float = 0.20) -> DriftReport:
    """
    Population Stability Index (PSI) sur les prédictions.

    Interprétation :
      PSI < 0.10 → distribution stable, pas d'action
      0.10 ≤ PSI < 0.20 → légère dérive, surveiller
      PSI ≥ 0.20 → dérive significative, réentraîner
    """
    # Normaliser les prédictions pour le binning
    bins = np.percentile(y_pred_reference, np.linspace(0, 100, n_bins + 1))
    bins[0]  -= 1e-6
    bins[-1] += 1e-6

    ref_counts, _ = np.histogram(y_pred_reference, bins=bins)
    cur_counts, _ = np.histogram(y_pred_current, bins=bins)

    ref_pct = ref_counts / len(y_pred_reference)
    cur_pct = cur_counts / len(y_pred_current)

    # Éviter la division par zéro
    ref_pct = np.where(ref_pct == 0, 1e-6, ref_pct)
    cur_pct = np.where(cur_pct == 0, 1e-6, cur_pct)

    psi = float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))
    drift_detected = psi >= threshold

    if psi < 0.10:
        recommendation = "Distribution stable — pas d'action."
    elif psi < 0.20:
        recommendation = "Légère dérive — augmenter la fréquence de monitoring."
    else:
        recommendation = "Dérive significative — réentraîner le modèle."

    return DriftReport(
        drift_detected=drift_detected,
        method="PSI",
        statistic=psi,
        threshold=threshold,
        details={"n_bins": n_bins, "psi_value": round(psi, 4)},
        recommendation=recommendation,
    )


def cusum_drift(errors: np.ndarray, target_mean: float = 0.0,
                k: float = 0.5, h: float = 5.0) -> DriftReport:
    """
    CUSUM (Cumulative Sum Control Chart) sur les erreurs de prédiction.
    Détecte un biais systématique qui se cumule dans le temps.

    Args:
        errors      : série d'erreurs (y_pred - y_true) en MW
        target_mean : biais attendu (0 pour un modèle non biaisé)
        k           : paramètre de sensibilité (0.5 × écart-type attendu)
        h           : seuil de détection (5 × écart-type attendu)
    """
    std_errors = np.std(errors)
    k_abs = k * std_errors
    h_abs = h * std_errors

    cusum_pos = np.zeros(len(errors))
    cusum_neg = np.zeros(len(errors))

    for i in range(1, len(errors)):
        cusum_pos[i] = max(0, cusum_pos[i-1] + (errors[i] - target_mean) - k_abs)
        cusum_neg[i] = max(0, cusum_neg[i-1] - (errors[i] - target_mean) - k_abs)

    max_cusum = max(cusum_pos.max(), cusum_neg.max())
    drift_detected = max_cusum > h_abs

    return DriftReport(
        drift_detected=drift_detected,
        method="CUSUM",
        statistic=max_cusum / std_errors if std_errors > 0 else 0.0,
        threshold=h,
        details={
            "max_cusum_pos": round(float(cusum_pos.max()), 2),
            "max_cusum_neg": round(float(cusum_neg.max()), 2),
            "std_errors_mw": round(float(std_errors), 2),
        },
        recommendation=(
            "Biais cumulatif détecté — vérifier les données récentes et réentraîner."
            if drift_detected else
            "Erreurs centrées autour de zéro — modèle stable."
        ),
    )


def full_drift_analysis(X_reference: np.ndarray, X_current: np.ndarray,
                         y_pred_reference: np.ndarray, y_pred_current: np.ndarray,
                         errors_current: np.ndarray) -> dict:
    """
    Analyse complète de dérive combinant les 3 méthodes.
    Retourne un rapport consolidé avec recommandation globale.
    """
    ks_report   = ks_test_drift(X_reference, X_current)
    psi_report  = psi_drift(y_pred_reference, y_pred_current)
    cusum_report = cusum_drift(errors_current)

    any_drift = ks_report.drift_detected or psi_report.drift_detected or cusum_report.drift_detected
    n_alerts  = sum([
        ks_report.drift_detected, psi_report.drift_detected, cusum_report.drift_detected
    ])

    if n_alerts == 0:
        global_recommendation = " Modèle stable — surveillance normale (vérification mensuelle)."
    elif n_alerts == 1:
        global_recommendation = "  Signal faible — augmenter la fréquence de monitoring (hebdomadaire)."
    else:
        global_recommendation = " Dérive confirmée — réentraînement urgent requis sous 48h."

    report = {
        "drift_detected": any_drift,
        "n_alerts": n_alerts,
        "global_recommendation": global_recommendation,
        "ks_test":  {"drift": ks_report.drift_detected,  "stat": ks_report.statistic},
        "psi":      {"drift": psi_report.drift_detected,  "stat": psi_report.statistic},
        "cusum":    {"drift": cusum_report.drift_detected, "stat": cusum_report.statistic},
    }

    logger.info(f"Analyse dérive complète — alertes={n_alerts}/3 | dérive={any_drift}")
    for r in [ks_report, psi_report, cusum_report]:
        logger.info(str(r))

    return report
