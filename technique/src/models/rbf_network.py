"""
Implémentation d'un Réseau de Neurones RBF (Radial Basis Function).

Architecture :
  Couche d'entrée → Couche cachée RBF (fonctions gaussiennes, centres = K-Means)
                  → Couche de sortie linéaire (Ridge Regression)

Références :
  - Broomhead & Lowe (1988) — Multivariable functional interpolation and adaptive networks
  - Orr (1996) — Introduction to Radial Basis Function Networks
"""

import numpy as np
import joblib
import logging
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge
from sklearn.utils.validation import check_is_fitted

logger = logging.getLogger(__name__)


class RBFNetwork(BaseEstimator, RegressorMixin):
    """
    Réseau de neurones à fonctions de base radiales (RBF).

    Paramètres
    ----------
    n_centers : int
        Nombre de neurones dans la couche cachée RBF.
        Les centres sont déterminés par K-Means clustering.
    gamma : float
        Paramètre de largeur de la fonction gaussienne.
        Plus gamma est grand, plus les fonctions sont étroites.
    alpha : float
        Coefficient de régularisation L2 de la régression Ridge en sortie.
    random_state : int
        Graine aléatoire pour la reproductibilité.
    """

    def __init__(self, n_centers: int = 50, gamma: float = 1.0,
                 alpha: float = 0.01, random_state: int = 42):
        self.n_centers = n_centers
        self.gamma = gamma
        self.alpha = alpha
        self.random_state = random_state

    # ─────────────────────────────────────
    # Fonction d'activation RBF (Gaussienne)
    # ─────────────────────────────────────
    def _rbf_activation(self, X: np.ndarray, centers: np.ndarray) -> np.ndarray:
        """
        Calcule les activations gaussiennes pour chaque sample et chaque centre.

        φ(x, cᵢ) = exp(-γ · ||x - cᵢ||²)

        Args:
            X       : (n_samples, n_features)
            centers : (n_centers, n_features)

        Returns:
            H : (n_samples, n_centers) — matrice d'activations
        """
        # Calcul vectorisé : ||x - c||² pour tous les x et c simultanément
        # diff : (n_samples, n_centers, n_features)
        diff = X[:, np.newaxis, :] - centers[np.newaxis, :, :]
        dist_sq = np.sum(diff ** 2, axis=2)  # (n_samples, n_centers)
        return np.exp(-self.gamma * dist_sq)

    # ─────────────────────────────────────
    # Entraînement
    # ─────────────────────────────────────
    def fit(self, X: np.ndarray, y: np.ndarray) -> "RBFNetwork":
        """
        Entraîne le réseau RBF en deux étapes :
          1. Détermination des centres par K-Means (non supervisé)
          2. Apprentissage des poids de sortie par Ridge Regression

        Args:
            X : (n_samples, n_features) — features normalisées
            y : (n_samples,) — consommation cible en MW
        """
        logger.info(f"Entraînement RBF : n_centers={self.n_centers}, gamma={self.gamma}")

        # Étape 1 : Centres par K-Means
        kmeans = KMeans(
            n_clusters=self.n_centers,
            random_state=self.random_state,
            n_init=10,
            max_iter=300,
        )
        kmeans.fit(X)
        self.centers_ = kmeans.cluster_centers_  # (n_centers, n_features)
        logger.info(f"K-Means converged en {kmeans.n_iter_} itérations")

        # Étape 2 : Matrice d'activations H
        H = self._rbf_activation(X, self.centers_)  # (n_samples, n_centers)

        # Étape 3 : Poids de sortie via Ridge Regression
        self.output_layer_ = Ridge(alpha=self.alpha, fit_intercept=True)
        self.output_layer_.fit(H, y)

        self.n_features_in_ = X.shape[1]
        logger.info("Entraînement RBF terminé")
        return self

    # ─────────────────────────────────────
    # Inférence
    # ─────────────────────────────────────
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Prédit la consommation électrique pour de nouveaux échantillons.

        Args:
            X : (n_samples, n_features)

        Returns:
            y_pred : (n_samples,) — consommation prédite en MW
        """
        check_is_fitted(self, ["centers_", "output_layer_"])
        H = self._rbf_activation(X, self.centers_)
        return self.output_layer_.predict(H)

    # ─────────────────────────────────────
    # Persistance
    # ─────────────────────────────────────
    def save(self, path: str) -> None:
        """Sérialise le modèle entraîné avec joblib."""
        joblib.dump(self, path)
        logger.info(f"Modèle RBF sauvegardé → {path}")

    @classmethod
    def load(cls, path: str) -> "RBFNetwork":
        """Charge un modèle RBF sérialisé."""
        model = joblib.load(path)
        logger.info(f"Modèle RBF chargé depuis {path}")
        return model


if __name__ == "__main__":
    # Test rapide avec données aléatoires
    np.random.seed(42)
    X_test = np.random.randn(100, 14)
    y_test = np.random.rand(100) * 50000 + 30000

    rbf = RBFNetwork(n_centers=20, gamma=0.5, alpha=0.1)
    rbf.fit(X_test, y_test)
    y_pred = rbf.predict(X_test[:5])
    print("Prédictions test :", y_pred.round(0))
