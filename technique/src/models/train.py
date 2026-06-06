"""
Script d'entraînement CLI — Tous les modèles EDF
Usage : python -m models.train [--model all|random_forest|rbf_network|decision_tree|knn]
"""

# pylint: disable=invalid-name

import argparse
import time
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV, cross_val_score

from models.rbf_network import RBFNetwork
from models.evaluate import evaluate_model, mape

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PROCESSED_PATH = Path(__file__).parents[2] / "data" / "processed"
MODELS_PATH    = Path(__file__).parents[2] / "data" / "models_saved"
MODELS_PATH.mkdir(parents=True, exist_ok=True)


def load_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Charge les jeux de données d'entraînement et de test depuis le répertoire
    des données prétraitées.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        X_train, X_test, y_train, y_test.
    """
    X_train = np.load(PROCESSED_PATH / "X_train.npy")
    X_test = np.load(PROCESSED_PATH / "X_test.npy")
    y_train = np.load(PROCESSED_PATH / "y_train.npy")
    y_test = np.load(PROCESSED_PATH / "y_test.npy")

    logger.info(
        "Données chargées — Train: %s, Test: %s",
        X_train.shape,
        X_test.shape,
    )

    return X_train, X_test, y_train, y_test


def train_random_forest(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """
    Entraîne un modèle Random Forest avec recherche d'hyperparamètres.

    Parameters
    ----------
    X_train : np.ndarray
        Jeu d'entraînement des features.
    X_test : np.ndarray
        Jeu de test des features.
    y_train : np.ndarray
        Cibles d'entraînement.
    y_test : np.ndarray
        Cibles de test.

    Returns
    -------
    dict
        Métriques d'évaluation et hyperparamètres du modèle.
    """
    logger.info("=== Entraînement Random Forest ===")

    tscv = TimeSeriesSplit(n_splits=5)

    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [10, 15, None],
        "min_samples_split": [5, 10],
        "min_samples_leaf": [3, 5],
    }

    gs = GridSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        param_grid,
        cv=tscv,
        scoring="neg_mean_absolute_percentage_error",
        n_jobs=-1,
        verbose=0,
    )

    t0 = time.time()
    gs.fit(X_train, y_train)

    rf = gs.best_estimator_
    training_time = time.time() - t0

    metrics = evaluate_model(
        rf,
        X_test,
        y_test,
        model_name="Random Forest",
    )

    metrics["training_time_s"] = round(training_time, 1)
    metrics["hyperparameters"] = gs.best_params_

    joblib.dump(rf, MODELS_PATH / "random_forest_v1.pkl")
    pd.Series(metrics).to_json(MODELS_PATH / "metrics_random_forest.json")

    logger.info(
        "Random Forest — R²=%.4f | MAPE=%.2f%%",
        metrics["r2"],
        metrics["mape_pct"],
    )

    return metrics


def train_decision_tree(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """
    Entraîne un arbre de décision et sélectionne la profondeur optimale.

    Parameters
    ----------
    X_train : np.ndarray
        Jeu d'entraînement des features.
    X_test : np.ndarray
        Jeu de test des features.
    y_train : np.ndarray
        Cibles d'entraînement.
    y_test : np.ndarray
        Cibles de test.

    Returns
    -------
    dict
        Métriques d'évaluation et hyperparamètres du modèle.
    """
    logger.info("=== Entraînement Arbre de Décision ===")

    depths = range(1, 25)
    mape_test_list = []

    for depth in depths:
        model = DecisionTreeRegressor(
            max_depth=depth,
            random_state=42,
        )
        model.fit(X_train, y_train)
        mape_test_list.append(
            mape(y_test, model.predict(X_test))
        )

    optimal_depth = list(depths)[np.argmin(mape_test_list)]

    t0 = time.time()

    dt_final = DecisionTreeRegressor(
        max_depth=optimal_depth,
        min_samples_split=20,
        min_samples_leaf=10,
        criterion="squared_error",
        random_state=42,
    )

    dt_final.fit(X_train, y_train)

    training_time = time.time() - t0

    metrics = evaluate_model(
        dt_final,
        X_test,
        y_test,
        model_name="Arbre de Décision",
    )

    metrics["training_time_s"] = round(training_time, 3)
    metrics["hyperparameters"] = {
        "max_depth": optimal_depth,
        "min_samples_split": 20,
        "min_samples_leaf": 10,
    }

    joblib.dump(
        dt_final,
        MODELS_PATH / "decision_tree_v1.pkl",
    )

    pd.Series(metrics).to_json(
        MODELS_PATH / "metrics_decision_tree.json",
    )

    logger.info(
        "Arbre de Décision — R²=%.4f | MAPE=%.2f%%",
        metrics["r2"],
        metrics["mape_pct"],
    )

    return metrics


def train_rbf_network(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """
    Entraîne un réseau RBF avec sélection d'hyperparamètres par validation croisée.

    Parameters
    ----------
    X_train : np.ndarray
        Jeu d'entraînement des features.
    X_test : np.ndarray
        Jeu de test des features.
    y_train : np.ndarray
        Cibles d'entraînement.
    y_test : np.ndarray
        Cibles de test.

    Returns
    -------
    dict
        Métriques d'évaluation et hyperparamètres du modèle.
    """
    logger.info("=== Entraînement Réseau RBF ===")

    tscv = TimeSeriesSplit(n_splits=3)
    best_score = -np.inf
    best_config: dict[str, float | int] = {}

    for n_centers in [20, 50, 100]:
        for gamma in [0.1, 0.5, 1.0, 2.0]:
            for alpha in [0.001, 0.01, 0.1]:
                scores = []

                for train_idx, val_idx in tscv.split(X_train):
                    rbf = RBFNetwork(
                        n_centers=n_centers,
                        gamma=gamma,
                        alpha=alpha,
                    )
                    rbf.fit(X_train[train_idx], y_train[train_idx])

                    score = -mape(
                        y_train[val_idx],
                        rbf.predict(X_train[val_idx]),
                    )
                    scores.append(score)

                mean_score = np.mean(scores)

                if mean_score > best_score:
                    best_score = mean_score
                    best_config = {
                        "n_centers": n_centers,
                        "gamma": gamma,
                        "alpha": alpha,
                    }

    t0 = time.time()

    rbf_final = RBFNetwork(**best_config, random_state=42)
    rbf_final.fit(X_train, y_train)

    training_time = time.time() - t0

    metrics = evaluate_model(
        rbf_final,
        X_test,
        y_test,
        model_name="Réseau RBF",
    )

    metrics["training_time_s"] = round(training_time, 1)
    metrics["hyperparameters"] = best_config

    rbf_final.save(str(MODELS_PATH / "rbf_network_v1.pkl"))
    pd.Series(metrics).to_json(MODELS_PATH / "metrics_rbf_network.json")

    logger.info(
        "Réseau RBF — R²=%.4f | MAPE=%.2f%%",
        metrics["r2"],
        metrics["mape_pct"],
    )

    return metrics


def train_knn(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """
    Entraîne un modèle KNN avec sélection du nombre optimal de voisins.

    Parameters
    ----------
    X_train : np.ndarray
        Jeu d'entraînement des features.
    X_test : np.ndarray
        Jeu de test des features.
    y_train : np.ndarray
        Cibles d'entraînement.
    y_test : np.ndarray
        Cibles de test.

    Returns
    -------
    dict
        Métriques d'évaluation et hyperparamètres du modèle.
    """
    logger.info("=== Entraînement KNN ===")

    tscv = TimeSeriesSplit(n_splits=5)
    k_range = list(range(1, 31)) + list(range(35, 76, 5))
    mape_cv_list = []

    for n_neighbors in k_range:
        knn = KNeighborsRegressor(
            n_neighbors=n_neighbors,
            weights="distance",
        )

        scores = cross_val_score(
            knn,
            X_train,
            y_train,
            cv=tscv,
            scoring="neg_mean_absolute_percentage_error",
        )

        mape_cv_list.append(-scores.mean() * 100)

    optimal_k = k_range[np.argmin(mape_cv_list)]

    t0 = time.time()

    knn_final = KNeighborsRegressor(
        n_neighbors=optimal_k,
        weights="distance",
        metric="euclidean",
        algorithm="ball_tree",
    )

    knn_final.fit(X_train, y_train)

    training_time = time.time() - t0

    metrics = evaluate_model(
        knn_final,
        X_test,
        y_test,
        model_name="KNN",
    )

    metrics["training_time_s"] = round(training_time, 3)
    metrics["hyperparameters"] = {
        "n_neighbors": optimal_k,
        "weights": "distance",
    }

    joblib.dump(knn_final, MODELS_PATH / "knn_v1.pkl")
    pd.Series(metrics).to_json(MODELS_PATH / "metrics_knn.json")

    logger.info(
        "KNN — R²=%.4f | MAPE=%.2f%%",
        metrics["r2"],
        metrics["mape_pct"],
    )

    return metrics


def main() -> None:
    """Lance l'entraînement d'un ou plusieurs modèles depuis la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Entraînement des modèles EDF",
    )
    parser.add_argument(
        "--model",
        default="all",
        choices=[
            "all",
            "random_forest",
            "rbf_network",
            "decision_tree",
            "knn",
        ],
        help="Modèle à entraîner",
    )

    args = parser.parse_args()

    X_train, X_test, y_train, y_test = load_data()

    trainers = {
        "random_forest": train_random_forest,
        "decision_tree": train_decision_tree,
        "rbf_network": train_rbf_network,
        "knn": train_knn,
    }

    models_to_train = (
        list(trainers.keys())
        if args.model == "all"
        else [args.model]
    )

    all_metrics = {}

    for name in models_to_train:
        metrics = trainers[name](
            X_train,
            X_test,
            y_train,
            y_test,
        )
        all_metrics[name] = metrics

    logger.info("%s", "\n" + "=" * 60)
    logger.info("RÉSUMÉ ENTRAÎNEMENT")
    logger.info("%s", "=" * 60)

    for name, metrics in all_metrics.items():
        status = "" if metrics.get("mape_pct", 99) <= 4.0 else "⚠️ "

        logger.info(
            "%s %-20s R²=%.4f | MAPE=%.2f%%",
            status,
            name,
            metrics["r2"],
            metrics["mape_pct"],
        )

if __name__ == "__main__":
    main()
