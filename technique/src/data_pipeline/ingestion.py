"""
Ingestion des données RTE éco2mix et Météo France.
Collecte quotidienne orchestrée par Apache Airflow.

Priorité de chargement dans fetch_rte_eco2mix() :
  1. API RTE OAuth2   (Option B) — si client_id/client_secret fournis
  2. Fichiers XLS locaux data/data_RTE/  (Option A) — fichiers eco2mix téléchargés
  3. Données synthétiques             (fallback)

Température :
  fetch_temperature_nationale() interroge l'API Open-Meteo (gratuite, sans clé)
  et calcule une moyenne sur 8 villes françaises représentatives.
  Résultat mis en cache dans data/raw/temperature_nationale_DEBUT_FIN.csv.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Répertoire pour les fichiers bruts générés / téléchargés
RAW_DATA_PATH = Path(__file__).parents[2] / "data" / "raw"
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# Répertoire contenant les fichiers XLS éco2mix officiels (Option A)
XLS_DATA_PATH = Path(__file__).parents[2] / "data" / "data_RTE"


# ─────────────────────────────────────────────────────────────
# 1. POINT D'ENTRÉE PRINCIPAL
# ─────────────────────────────────────────────────────────────

def fetch_rte_eco2mix(date_debut: str, date_fin: str,
                      rte_client_id: str = None,
                      rte_client_secret: str = None) -> pd.DataFrame:
    """
    Charge les données de consommation électrique RTE éco2mix.

    Priorité :
      1. API RTE OAuth2  si client_id et client_secret sont fournis  (Option B)
      2. Fichiers XLS locaux dans data/data_RTE/                     (Option A)
      3. Données synthétiques réalistes                              (fallback)

    Args:
        date_debut:         Format 'YYYY-MM-DD'
        date_fin:           Format 'YYYY-MM-DD'
        rte_client_id:      Client ID OAuth2 RTE (optionnel, pour Option B)
        rte_client_secret:  Client Secret OAuth2 RTE (optionnel, pour Option B)

    Returns:
        DataFrame journalier avec colonnes standardisées
        [date, consommation_mw, temperature_moyenne, temperature_min,
         temperature_max, type_jour, mois, jour_semaine, jour_annee]
    """
    # ── Option B : API RTE OAuth2
    if rte_client_id and rte_client_secret:
        try:
            return fetch_rte_eco2mix_api(date_debut, date_fin,
                                         rte_client_id, rte_client_secret)
        except NotImplementedError:
            logger.warning("API RTE non implémentée — passage au chargement local")
        except Exception as e:
            logger.warning(f"Erreur API RTE : {e} — passage au chargement local")

    # ── Option A : fichiers XLS locaux
    df = _load_rte_xls_directory(XLS_DATA_PATH, date_debut, date_fin)
    if not df.empty:
        return df

    # ── Fallback : données synthétiques
    logger.warning("Aucune donnée RTE trouvée — génération de données synthétiques réalistes")
    return generate_synthetic_data(date_debut, date_fin)


# ─────────────────────────────────────────────────────────────
# 2. OPTION B — API RTE OAuth2 (stub à implémenter)
# ─────────────────────────────────────────────────────────────

def fetch_rte_eco2mix_api(date_debut: str, date_fin: str,
                           client_id: str, client_secret: str) -> pd.DataFrame:
    """
    Option B — Appel direct à l'API RTE Open Data via OAuth2.

    Pour activer :
      1. Créer un compte sur https://data.rte-france.com/
      2. Créer une application et récupérer client_id / client_secret
      3. Appeler fetch_rte_eco2mix(..., rte_client_id=..., rte_client_secret=...)

    Endpoints utiles :
      - Consommation réalisée : /open_api/consumption/v1/short_term
      - Bilan éco2mix         : /open_api/eco2mix/v3/actual_generations_per_unit

    Note : l'API ne fournit pas d'historique au-delà de quelques semaines.
    Pour les données historiques (2019-2024), utiliser les fichiers XLS (Option A).
    """
    raise NotImplementedError(
        "L'API RTE OAuth2 n'est pas encore implémentée. "
        "Inscrivez-vous sur https://data.rte-france.com/ et complétez cette fonction."
    )

    # ── Squelette d'implémentation OAuth2 RTE ──────────────────
    # token_url = "https://digital.iservices.rte-france.com/token/oauth/"
    # import base64
    # credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    # resp = requests.post(token_url, headers={"Authorization": f"Basic {credentials}"})
    # resp.raise_for_status()
    # access_token = resp.json()["access_token"]
    #
    # api_url = "https://digital.iservices.rte-france.com/open_api/consumption/v1/short_term"
    # params = {"start_date": f"{date_debut}T00:00:00+02:00",
    #           "end_date":   f"{date_fin}T23:59:59+02:00"}
    # resp = requests.get(api_url,
    #                     headers={"Authorization": f"Bearer {access_token}"},
    #                     params=params)
    # resp.raise_for_status()
    # raw = resp.json()
    # ... parser raw et retourner un DataFrame standardisé


# ─────────────────────────────────────────────────────────────
# 3. MÉTÉO — API Open-Meteo (gratuite, sans clé)
# ─────────────────────────────────────────────────────────────

# 8 villes représentatives de la diversité climatique française
_VILLES_METEO = [
    ("Paris",      48.8566,  2.3522),
    ("Lyon",       45.7640,  4.8357),
    ("Marseille",  43.2965,  5.3698),
    ("Bordeaux",   44.8378, -0.5792),
    ("Lille",      50.6292,  3.0573),
    ("Strasbourg", 48.5734,  7.7521),
    ("Nantes",     47.2184, -1.5536),
    ("Toulouse",   43.6047,  1.4442),
]

_OPENMETEO_URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_temperature_nationale(date_debut: str, date_fin: str,
                                 use_cache: bool = True) -> pd.DataFrame:
    """
    Récupère les températures journalières françaises depuis l'API Open-Meteo.

    API gratuite, sans clé, données ERA5 disponibles depuis 1940.
    Calcule une moyenne pondérée sur 8 villes représentatives.
    Le résultat est mis en cache dans data/raw/ pour éviter les appels répétés.

    Args:
        date_debut:  Format 'YYYY-MM-DD'
        date_fin:    Format 'YYYY-MM-DD'
        use_cache:   Si True, charge depuis le cache si disponible

    Returns:
        DataFrame avec colonnes [date, temperature_moyenne, temperature_min, temperature_max]
        DataFrame vide si toutes les requêtes échouent.
    """
    cache_path = RAW_DATA_PATH / f"temperature_nationale_{date_debut}_{date_fin}.csv"

    if use_cache and cache_path.exists():
        logger.info(f"Température chargée depuis le cache : {cache_path.name}")
        df = pd.read_csv(cache_path, parse_dates=["date"])
        return df

    logger.info(f"Récupération des températures via Open-Meteo ({len(_VILLES_METEO)} villes)…")
    dfs_villes = []

    for ville, lat, lon in _VILLES_METEO:
        try:
            resp = requests.get(
                _OPENMETEO_URL,
                params={
                    "latitude":   lat,
                    "longitude":  lon,
                    "start_date": date_debut,
                    "end_date":   date_fin,
                    "daily":      "temperature_2m_mean,temperature_2m_min,temperature_2m_max",
                    "timezone":   "Europe/Paris",
                },
                timeout=30,
            )
            resp.raise_for_status()
            daily = resp.json()["daily"]
            df_ville = pd.DataFrame({
                "date":    pd.to_datetime(daily["time"]),
                "t_mean":  daily["temperature_2m_mean"],
                "t_min":   daily["temperature_2m_min"],
                "t_max":   daily["temperature_2m_max"],
            })
            df_ville["ville"] = ville
            dfs_villes.append(df_ville)
            logger.info(f"  ✓ {ville}")
        except Exception as e:
            logger.warning(f"  ✗ {ville} : {e}")

    if not dfs_villes:
        logger.error("Aucune donnée météo récupérée — toutes les requêtes ont échoué")
        return pd.DataFrame()

    df_all = pd.concat(dfs_villes, ignore_index=True)

    # Moyenne nationale (moyenne simple des 8 villes)
    df_meteo = (
        df_all.groupby("date", as_index=False)
        .agg(
            temperature_moyenne=("t_mean", "mean"),
            temperature_min=("t_min", "mean"),
            temperature_max=("t_max", "mean"),
        )
    )
    df_meteo["temperature_moyenne"] = df_meteo["temperature_moyenne"].round(1)
    df_meteo["temperature_min"]     = df_meteo["temperature_min"].round(1)
    df_meteo["temperature_max"]     = df_meteo["temperature_max"].round(1)

    df_meteo.to_csv(cache_path, index=False)
    logger.info(
        f"Températures sauvegardées ({len(df_meteo)} jours) → {cache_path.name}  "
        f"[{len(dfs_villes)}/{len(_VILLES_METEO)} villes]"
    )
    return df_meteo


# ─────────────────────────────────────────────────────────────
# 4. OPTION A — Chargement des fichiers XLS locaux
# ─────────────────────────────────────────────────────────────

def _load_rte_xls_directory(data_dir: Path, date_debut: str, date_fin: str) -> pd.DataFrame:
    """
    Charge et agrège les fichiers XLS éco2mix officiels (format TSV latin-1)
    en un DataFrame journalier.

    Les fichiers sont nommés : eCO2mix_RTE_Annuel-Definitif_YYYY.xls
    Ils contiennent des données au pas de 15 minutes pour toute la France.
    """
    if not data_dir.exists():
        logger.warning(f"Répertoire XLS introuvable : {data_dir}")
        return pd.DataFrame()

    xls_files = sorted(data_dir.glob("eCO2mix_RTE_Annuel-Definitif_*.xls"))
    if not xls_files:
        logger.warning(f"Aucun fichier XLS éco2mix dans {data_dir}")
        return pd.DataFrame()

    # Filtrer par années couvertes par la période demandée
    year_debut = pd.Timestamp(date_debut).year
    year_fin = pd.Timestamp(date_fin).year
    xls_files = [
        f for f in xls_files
        if any(str(y) in f.name for y in range(year_debut, year_fin + 1))
    ]

    if not xls_files:
        logger.warning(f"Aucun fichier XLS pour la période {date_debut} → {date_fin}")
        return pd.DataFrame()

    dfs = []
    for path in xls_files:
        try:
            # Les fichiers éco2mix sont des TSV latin-1 avec extension .xls
            # index_col=False évite que pandas traite la 1re colonne comme index
            df = pd.read_csv(path, sep="\t", encoding="latin-1", index_col=False,
                             low_memory=False)
            dfs.append(df)
            logger.info(f"Chargé : {path.name}  ({len(df):,} lignes)")
        except Exception as e:
            logger.warning(f"Impossible de lire {path.name} : {e}")

    if not dfs:
        return pd.DataFrame()

    df_raw = pd.concat(dfs, ignore_index=True)

    # Colonnes attendues (après index_col=False) :
    #   Périmètre | Nature | Date (YYYY-MM-DD) | Heures (HH:MM) | Consommation | …
    df_raw["_date"] = pd.to_datetime(df_raw["Date"], format="%Y-%m-%d", errors="coerce")
    df_raw["_conso"] = pd.to_numeric(df_raw["Consommation"], errors="coerce")

    df_raw = df_raw.dropna(subset=["_date", "_conso"])
    df_raw = df_raw[
        (df_raw["_date"] >= date_debut) & (df_raw["_date"] <= date_fin)
    ]

    if df_raw.empty:
        logger.warning("Aucune donnée valide après filtrage de la période")
        return pd.DataFrame()

    # Agrégation journalière (moyenne des relevés 15 min non NaN)
    df_daily = (
        df_raw.groupby("_date", as_index=False)
        .agg(consommation_mw=("_conso", "mean"))
        .rename(columns={"_date": "date"})
    )
    df_daily["consommation_mw"] = df_daily["consommation_mw"].round(0)

    # Ajout des features temporelles + météo synthétique
    df_daily = _enrich_daily(df_daily)

    logger.info(
        f"Données RTE XLS chargées : {len(df_daily)} jours  "
        f"({df_daily['date'].min().date()} → {df_daily['date'].max().date()})"
    )
    return df_daily


def _enrich_daily(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute les features temporelles et les températures réelles (Open-Meteo).
    Fallback sur température synthétique si l'API est indisponible.
    """
    df = df.copy()
    dates = pd.DatetimeIndex(df["date"])
    n = len(df)

    jour_annee  = dates.dayofyear
    jour_semaine = dates.dayofweek
    feries = _liste_jours_feries(dates)

    df["type_jour"]    = np.where(feries, 2, np.where(jour_semaine >= 5, 1, 0))
    df["mois"]         = dates.month
    df["jour_semaine"] = jour_semaine
    df["jour_annee"]   = jour_annee

    # ── Températures réelles via Open-Meteo
    date_debut = df["date"].min().strftime("%Y-%m-%d")
    date_fin   = df["date"].max().strftime("%Y-%m-%d")
    df_meteo = fetch_temperature_nationale(date_debut, date_fin)

    if not df_meteo.empty:
        df = df.merge(df_meteo, on="date", how="left")
        missing = df["temperature_moyenne"].isna().sum()
        if missing > 0:
            logger.warning(f"{missing} jours sans données météo — interpolation linéaire")
            df[["temperature_moyenne", "temperature_min", "temperature_max"]] = (
                df[["temperature_moyenne", "temperature_min", "temperature_max"]]
                .interpolate(method="linear")
            )
    else:
        # ── Fallback synthétique
        logger.warning("API météo indisponible — utilisation de températures synthétiques")
        np.random.seed(42)
        temperature = 12 - 10 * np.cos(2 * np.pi * (jour_annee - 15) / 365)
        temperature += np.random.normal(0, 2, n)
        df["temperature_moyenne"] = temperature.round(1)
        df["temperature_min"]  = (temperature - np.abs(np.random.normal(3, 1, n))).round(1)
        df["temperature_max"]  = (temperature + np.abs(np.random.normal(4, 1, n))).round(1)

    return df


# ─────────────────────────────────────────────────────────────
# 5. FALLBACK — Données synthétiques
# ─────────────────────────────────────────────────────────────

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

    jour_annee = dates.dayofyear
    saisonnalite = 10_000 * np.cos(2 * np.pi * (jour_annee - 15) / 365)

    temperature = 12 - 10 * np.cos(2 * np.pi * (jour_annee - 15) / 365)
    temperature += np.random.normal(0, 2, n)

    seuil_chauffe = 17.0
    effet_temperature = np.where(
        temperature < seuil_chauffe,
        (seuil_chauffe - temperature) * 2_500,
        0
    )

    jour_semaine = dates.dayofweek
    effet_semaine = np.where(jour_semaine >= 5, -4_500, 0)

    feries = _liste_jours_feries(dates)
    effet_ferie = np.where(feries, -6_000, 0)

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
    """Identifie les jours fériés français (jours fixes uniquement)."""
    feries = np.zeros(len(dates), dtype=bool)
    jours_fixes = {(1, 1), (5, 1), (5, 8), (7, 14), (8, 15), (11, 1), (11, 11), (12, 25)}
    for i, d in enumerate(dates):
        if (d.month, d.day) in jours_fixes:
            feries[i] = True
    return feries


# ─────────────────────────────────────────────────────────────
# 6. AGRÉGATION JOURNALIÈRE (utilitaire)
# ─────────────────────────────────────────────────────────────

def aggregate_daily(df_horaire: pd.DataFrame) -> pd.DataFrame:
    """Agrège des données infra-journalières en données journalières."""
    if "date" not in df_horaire.columns:
        raise ValueError("La colonne 'date' est requise")

    agg = {"consommation_mw": ("consommation_mw", "mean")}
    if "temperature_moyenne" in df_horaire.columns:
        agg["temperature_moyenne"] = ("temperature_moyenne", "mean")

    return df_horaire.groupby("date").agg(**agg).reset_index()


# ─────────────────────────────────────────────────────────────
# 7. PIPELINE COMPLET D'INGESTION
# ─────────────────────────────────────────────────────────────

def run_ingestion_pipeline(date_debut: str = "2019-01-01",
                            date_fin: str = "2024-12-31",
                            rte_client_id: str = None,
                            rte_client_secret: str = None) -> pd.DataFrame:
    """Point d'entrée principal du pipeline d'ingestion."""
    logger.info(f"Lancement ingestion : {date_debut} → {date_fin}")

    df = fetch_rte_eco2mix(date_debut, date_fin, rte_client_id, rte_client_secret)

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
    print(f"Source : {'synthétique' if df['consommation_mw'].std() < 5000 else 'RTE XLS'}")
