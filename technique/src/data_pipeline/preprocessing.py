"""
Prétraitement des données : nettoyage, feature engineering, normalisation.
Prépare les datasets train/test pour les 4 modèles ML.
"""

import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

PROCESSED_PATH = Path(__file__).parents[2] / "data" / "processed"
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# 1. NETTOYAGE
# ─────────────────────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie le DataFrame brut :
      - Suppression des doublons
      - Traitement des valeurs manquantes (interpolation linéaire)
      - Détection et correction des outliers (IQR)
    """
    logger.info(f"Nettoyage : {len(df)} lignes initiales")

    # Tri chronologique
    df = df.sort_values("date").reset_index(drop=True)

    # Suppression doublons
    df = df.drop_duplicates(subset=["date"])

    # ── Valeurs manquantes ──
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    missing_before = df[numeric_cols].isnull().sum().sum()

    # Interpolation linéaire (≤ 3 valeurs consécutives manquantes)
    df[numeric_cols] = df[numeric_cols].interpolate(method="linear", limit=3)

    # Remplissage des restantes par la médiane
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    missing_after = df[numeric_cols].isnull().sum().sum()
    logger.info(f"Valeurs manquantes : {missing_before} → {missing_after}")

    # ── Outliers sur consommation_mw (IQR) ──
    if "consommation_mw" in df.columns:
        Q1 = df["consommation_mw"].quantile(0.25)
        Q3 = df["consommation_mw"].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 3 * IQR, Q3 + 3 * IQR

        outliers = ((df["consommation_mw"] < lower) | (df["consommation_mw"] > upper)).sum()
        logger.info(f"Outliers détectés (consommation_mw) : {outliers}")

        # Remplacement par la médiane glissante sur 7 jours
        df["consommation_mw"] = df["consommation_mw"].clip(lower, upper)

    logger.info(f"Nettoyage terminé : {len(df)} lignes conservées")
    return df


# ─────────────────────────────────────────────────────────────
# 2. FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée les variables explicatives (features) à partir des données brutes.

    Features créées :
      - consommation_j1   : consommation J-1 (lagged)
      - consommation_j7   : consommation J-7 (même jour semaine dernière)
      - consommation_ma7  : moyenne mobile 7 jours
      - temperature_*     : données météo
      - type_jour_*       : One-Hot Encoding (ouvré / weekend / férié)
      - mois, jour_semaine : cyclical encoding
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # ── Lag features ──
    df["consommation_j1"] = df["consommation_mw"].shift(1)
    df["consommation_j7"] = df["consommation_mw"].shift(7)
    df["consommation_j14"] = df["consommation_mw"].shift(14)

    # ── Moyenne mobile 7 jours (J-1 à J-7) ──
    df["consommation_ma7"] = df["consommation_mw"].shift(1).rolling(7).mean()

    # ── Encodage cyclique du mois (sin/cos pour préserver la circularité) ──
    df["mois_sin"] = np.sin(2 * np.pi * df["mois"] / 12)
    df["mois_cos"] = np.cos(2 * np.pi * df["mois"] / 12)

    # ── Encodage cyclique du jour de la semaine ──
    df["jour_sin"] = np.sin(2 * np.pi * df["jour_semaine"] / 7)
    df["jour_cos"] = np.cos(2 * np.pi * df["jour_semaine"] / 7)

    # ── One-Hot Encoding type_jour (0=ouvré, 1=week-end, 2=férié) ──
    df["est_ouvre"]  = (df["type_jour"] == 0).astype(int)
    df["est_weekend"] = (df["type_jour"] == 1).astype(int)
    df["est_ferie"]  = (df["type_jour"] == 2).astype(int)

    # ── Indicateur hiver (novembre à mars) ──
    df["est_hiver"] = df["mois"].isin([11, 12, 1, 2, 3]).astype(int)

    # Suppression des lignes avec NaN dues aux lags (7 premiers jours)
    df = df.dropna(subset=["consommation_j1", "consommation_j7"]).reset_index(drop=True)

    logger.info(f"Feature engineering terminé : {df.shape[1]} colonnes, {len(df)} lignes")
    return df


def get_feature_columns() -> list:
    """Retourne la liste ordonnée des colonnes utilisées comme features."""
    return [
        "consommation_j1",
        "consommation_j7",
        "consommation_ma7",
        "temperature_moyenne",
        "temperature_min",
        "temperature_max",
        "mois_sin",
        "mois_cos",
        "jour_sin",
        "jour_cos",
        "est_ouvre",
        "est_weekend",
        "est_ferie",
        "est_hiver",
    ]


TARGET_COLUMN = "consommation_mw"


# ─────────────────────────────────────────────────────────────
# 3. SPLIT ET NORMALISATION
# ─────────────────────────────────────────────────────────────

def split_train_test(df: pd.DataFrame,
                     feature_cols: list = None,
                     test_size: float = 0.2,
                     random_state: int = 42):
    """
    Sépare le dataset en train (80%) et test (20%).
    On utilise un split temporel (pas random) pour respecter la causalité.
    """
    feature_cols = feature_cols or get_feature_columns()
    available = [c for c in feature_cols if c in df.columns]

    X = df[available].values
    y = df[TARGET_COLUMN].values

    # Split temporel : les derniers 20% du temps → test
    split_idx = int(len(df) * (1 - test_size))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    logger.info(f"Split train/test : {len(X_train)} / {len(X_test)}")
    return X_train, X_test, y_train, y_test


def normalize_features(X_train: np.ndarray,
                        X_test: np.ndarray,
                        scaler_path: str = None):
    """
    Normalise les features avec StandardScaler (moyenne=0, std=1).
    Sauvegarde le scaler pour l'inférence en production.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    if scaler_path:
        joblib.dump(scaler, scaler_path)
        logger.info(f"Scaler sauvegardé → {scaler_path}")

    return X_train_scaled, X_test_scaled, scaler


# ─────────────────────────────────────────────────────────────
# 4. PIPELINE COMPLET
# ─────────────────────────────────────────────────────────────

def run_preprocessing_pipeline(df_raw: pd.DataFrame,
                                save: bool = True) -> dict:
    """
    Pipeline complet : nettoyage → feature engineering → split → normalisation.

    Returns:
        dict avec X_train, X_test, y_train, y_test, scaler, feature_cols, df_processed
    """
    df_clean = clean_data(df_raw)
    df_feat = build_features(df_clean)

    feature_cols = get_feature_columns()
    X_train, X_test, y_train, y_test = split_train_test(df_feat, feature_cols)

    scaler_path = str(PROCESSED_PATH / "scaler.pkl") if save else None
    X_train_sc, X_test_sc, scaler = normalize_features(X_train, X_test, scaler_path)

    if save:
        df_feat.to_parquet(PROCESSED_PATH / "dataset_processed.parquet", index=False)
        np.save(PROCESSED_PATH / "X_train.npy", X_train_sc)
        np.save(PROCESSED_PATH / "X_test.npy", X_test_sc)
        np.save(PROCESSED_PATH / "y_train.npy", y_train)
        np.save(PROCESSED_PATH / "y_test.npy", y_test)
        logger.info("Données traitées sauvegardées dans data/processed/")

    return {
        "X_train": X_train_sc,
        "X_test": X_test_sc,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler,
        "feature_cols": feature_cols,
        "df_processed": df_feat,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from ingestion import run_ingestion_pipeline

    df_raw = run_ingestion_pipeline()
    result = run_preprocessing_pipeline(df_raw)
    print(f"\nX_train shape : {result['X_train'].shape}")
    print(f"X_test shape  : {result['X_test'].shape}")
    print(f"Features      : {result['feature_cols']}")
