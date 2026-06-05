"""
Ingestion des données RTE éco2mix et Météo France.
Collecte quotidienne orchestrée par Apache Airflow.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path(__file__).parents[3] / "data" / "raw"
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# 1. DONNÉES RTE ÉCO2MIX
# ─────────────────────────────────────────────────────────────

def fetch_rte_eco2mix(date_debut: str, date_fin: str) -> pd.DataFrame:
    """
    Télécharge les données de consommation électrique depuis l'API RTE éco2mix.

    Args:
        date_debut: Format 'YYYY-MM-DD'
        date_fin:   Format 'YYYY-MM-DD'

    Returns:
        DataFrame avec colonnes [date, heure, consommation_mw, production_*]
    """
    # NOTE : En production, utiliser l'API RTE éco2mix avec credentials OAuth2
    # Pour le projet, on charge depuis CSV téléchargé manuellement

    csv_path = RAW_DATA_PATH / "rte_eco2mix_2019_2024.csv"
    if csv_path.exists():
        logger.info(f"Chargement depuis fichier local : {csv_path}")
        return _load_rte_csv(csv_path, date_debut, date_fin)

    logger.warning("Fichier RTE non trouvé — génération de données synthétiques réalistes")
    return generate_synthetic_data(date_debut, date_fin)


def _load_rte_csv(path: Path, date_debut: str, date_fin: str) -> pd.DataFrame:
    """Charge et nettoie les données depuis le CSV éco2mix officiel."""
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")

    # Nommage standard selon le format CSV RTE éco2mix
    col_map = {
        "Date": "date",
        "Heures": "heure",
        "Consommation": "consommation_mw",
        "Thermique": "prod_thermique",
        "Nucléaire": "prod_nucleaire",
        "Eolien": "prod_eolien",
        "Solaire": "prod_solaire",
        "Hydraulique": "prod_hydraulique",
        "Bioénergies": "prod_bioenergies",
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df = df.dropna(subset=["date", "consommation_mw"])
    df = df[(df["date"] >= date_debut) & (df["date"] <= date_fin)]

    return df.reset_index(drop=True)


def generate_synthetic_data(date_debut: str = "2019-01-01",
                             date_fin: str = "2024-12-31") -> pd.DataFrame:
    """
    Génère des données synthétiques réalistes mimant la consommation EDF.
    Basé sur les patterns réels du réseau français :
      - Base ~55 000 MW
      - Effet thermosensibilité : -3 500 MW/°C en dessous de 17°C
      - Creux week-end : -8 %
      - Creux estival (juillet-août) : -20 %
      - Pic hivernal (décembre-janvier) : +25 %
    """
    np.random.seed(42)
    dates = pd.date_range(date_debut, date_fin, freq="D")
    n = len(dates)

    # --- Saisonnalité annuelle (consommation de base)
    jour_annee = dates.dayofyear
    saisonnalite = 10_000 * np.cos(2 * np.pi * (jour_annee - 15) / 365)  # pic en janvier

    # --- Température synthétique (corrélée à la saisonnalité)
    temperature = 12 - 10 * np.cos(2 * np.pi * (jour_annee - 15) / 365)
    temperature += np.random.normal(0, 2, n)  # variabilité journalière

    # --- Thermosensibilité : effet chauffage électrique
    seuil_chauffe = 17.0
    effet_temperature = np.where(
        temperature < seuil_chauffe,
        (seuil_chauffe - temperature) * 2_500,
        0
    )

    # --- Effet jour de la semaine
    jour_semaine = dates.dayofweek  # 0=lundi, 6=dimanche
    effet_semaine = np.where(jour_semaine >= 5, -4_500, 0)  # week-end -8%

    # --- Jours fériés français (simplifié)
    feries = _liste_jours_feries(dates)
    effet_ferie = np.where(feries, -6_000, 0)

    # --- Consommation finale
    bruit = np.random.normal(0, 800, n)
    consommation = 52_000 + saisonnalite + effet_temperature + effet_semaine + effet_ferie + bruit
    consommation = np.clip(consommation, 25_000, 100_000)

    df = pd.DataFrame({
        "date": dates,
        "consommation_mw": consommation.round(0),
        "temperature_moyenne": temperature.round(1),
        "temperature_min": (temperature - np.abs(np.random.normal(3, 1, n))).round(1),
        "temperature_max": (temperature + np.abs(np.random.normal(4, 1, n))).round(1),
        "type_jour": np.where(feries, 2, np.where(jour_semaine >= 5, 1, 0)),
        "mois": dates.month,
        "jour_semaine": jour_semaine,
        "jour_annee": jour_annee,
    })

    output_path = RAW_DATA_PATH / "donnees_synthetiques.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Données synthétiques générées ({len(df)} jours) → {output_path}")

    return df


def _liste_jours_feries(dates: pd.DatetimeIndex) -> np.ndarray:
    """Identifie les jours fériés français (simplifié)."""
    feries = np.zeros(len(dates), dtype=bool)
    for i, d in enumerate(dates):
        mois_jour = (d.month, d.day)
        if mois_jour in [(1, 1), (5, 1), (5, 8), (7, 14), (8, 15),
                          (11, 1), (11, 11), (12, 25)]:
            feries[i] = True
    return feries


# ─────────────────────────────────────────────────────────────
# 2. AGRÉGATION JOURNALIÈRE
# ─────────────────────────────────────────────────────────────

def aggregate_daily(df_horaire: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège les données horaires en données journalières.
    (Utilisé si les données sont fournies à la granularité horaire)
    """
    if "date" not in df_horaire.columns:
        raise ValueError("La colonne 'date' est requise")

    df_daily = df_horaire.groupby("date").agg(
        consommation_mw=("consommation_mw", "mean"),
        temperature_moyenne=(
            ("temperature_moyenne", "mean")
            if "temperature_moyenne" in df_horaire.columns
            else ("consommation_mw", "count")
        ),
    ).reset_index()

    return df_daily


# ─────────────────────────────────────────────────────────────
# 3. PIPELINE COMPLET D'INGESTION
# ─────────────────────────────────────────────────────────────

def run_ingestion_pipeline(date_debut: str = "2019-01-01",
                            date_fin: str = "2024-12-31") -> pd.DataFrame:
    """Point d'entrée principal du pipeline d'ingestion."""
    logger.info(f"Lancement ingestion : {date_debut} → {date_fin}")

    df = fetch_rte_eco2mix(date_debut, date_fin)

    output_path = RAW_DATA_PATH / f"consommation_{date_debut}_{date_fin}.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Données sauvegardées → {output_path} ({len(df)} enregistrements)")

    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = run_ingestion_pipeline()
    print(df.head())
    print(f"\nShape : {df.shape}")
    print(f"Période : {df['date'].min()} → {df['date'].max()}")
    print(f"Consommation moyenne : {df['consommation_mw'].mean():.0f} MW")
