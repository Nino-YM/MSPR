"""
Configuration globale pytest — Projet EDF Prediction
"""
import sys
import os

# Ajouter le répertoire src au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
import numpy as np


@pytest.fixture(scope="session")
def sample_X():
    """Jeu de données X de test rapide (50 observations, 14 features)."""
    np.random.seed(42)
    return np.random.randn(50, 14)


@pytest.fixture(scope="session")
def sample_y():
    """Consommations électriques simulées (50 observations, en MW)."""
    np.random.seed(42)
    base = 55000
    return base + np.random.randn(50) * 5000
