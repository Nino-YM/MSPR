"""
Implémentation d'un Réseau de Neurones RBF (Radial Basis Function).

Architecture :
  Couche d'entrée → Couche cachée RBF (fonctions gaussiennes, centres = K-Means)
                  → Couche de sortie linéaire (Ridge Regression)

"""

import logging
import numpy as np
import joblib
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
    gamma : float
        Paramètre de largeur de la fonction gaussienne.
    alpha : float
        Coefficient de régularisation L2 de la régression Ridge en sortie.
    random_state : int
        Graine aléatoire pour la reproductibilité.
    """

    def __init__(
        self,
        n_centers: int = 50,
        gamma: float = 1.0,
        alpha: float = 0.01,
        random_state: int = 42,
    ) -> None:
        self.n_centers = n_centers
        self.gamma = gamma
        self.alpha = alpha
        self.random_state = random_state

        self.centers_: np.ndarray | None = None
        self.output_layer_: Ridge | None = None
        self.n_features_in_: int | None = None

    def _rbf_activation(self, x: np.ndarray, centers: np.ndarray) -> np.ndarray:
        """
        Calcule les activations gaussiennes pour chaque échantillon et chaque centre.

        φ(x, cᵢ) = exp(-γ · ||x - cᵢ||²)

        Parameters
        ----------
        x : np.ndarray
            Tableau de forme (n_samples, n_features).
        centers : np.ndarray
            Tableau de forme (n_centers, n_features).

        Returns
        -------
        np.ndarray
            Matrice d'activations de forme (n_samples, n_centers).
        """
        diff = x[:, np.newaxis, :] - centers[np.newaxis, :, :]
        dist_sq = np.sum(diff**2, axis=2)
        return np.exp(-self.gamma * dist_sq)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "RBFNetwork":
        """
        Entraîne le réseau RBF.

        Parameters
        ----------
        x : np.ndarray
            Features normalisées de forme (n_samples, n_features).
        y : np.ndarray
            Cible de forme (n_samples,).

        Returns
        -------
        RBFNetwork
            Instance entraînée.
        """
        logger.info(
            "Entraînement RBF : n_centers=%s, gamma=%s",
            self.n_centers,
            self.gamma,
        )

        kmeans = KMeans(
            n_clusters=self.n_centers,
            random_state=self.random_state,
            n_init=10,
            max_iter=300,
        )
        kmeans.fit(x)

        self.centers_ = kmeans.cluster_centers_

        logger.info(
            "K-Means converged en %s itérations",
            kmeans.n_iter_,
        )

        activation_matrix = self._rbf_activation(x, self.centers_)

        self.output_layer_ = Ridge(alpha=self.alpha, fit_intercept=True)
        self.output_layer_.fit(activation_matrix, y)

        self.n_features_in_ = x.shape[1]

        logger.info("Entraînement RBF terminé")

        return self
    # ─────────────────────────────────────
    # Inférence
    # ─────────────────────────────────────

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Prédit la consommation électrique pour de nouveaux échantillons.

        Args:
            X : (n_samples, n_features)

        Returns:
            y_pred : (n_samples,) — consommation prédite en MW
        """
        check_is_fitted(self, ["centers_", "output_layer_"])
        h = self._rbf_activation(x, self.centers_)
        return self.output_layer_.predict(h)

    # ─────────────────────────────────────
    # Persistance
    # ─────────────────────────────────────

    def save(self, path: str) -> None:
        """Sérialise le modèle entraîné avec joblib."""
        joblib.dump(self, path)
        logger.info("Modèle RBF sauvegardé → %s", path)


@classmethod
def load(_cls, path: str) -> "RBFNetwork":
    """Charge un modèle RBF sérialisé."""
    model = joblib.load(path)
    logger.info("Modèle RBF chargé depuis %s", path)
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
