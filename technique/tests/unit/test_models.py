"""
Tests unitaires — Modèles ML et Preprocessing
pytest tests/unit/test_models.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import numpy as np
import pytest
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

from models.rbf_network import RBFNetwork
from models.evaluate import r2_score, rmse, mape, accuracy_within_tolerance
from data_pipeline.preprocessing import (
    clean_data, build_features, get_feature_columns,
    split_train_test, normalize_features
)
from data_pipeline.ingestion import generate_synthetic_data


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def synthetic_dataset():
    """Dataset synthétique minimal pour les tests."""
    df = generate_synthetic_data("2020-01-01", "2022-12-31")
    return df


@pytest.fixture(scope="module")
def preprocessed_data(synthetic_dataset):
    """Données prétraitées prêtes pour l'entraînement."""
    df_clean = clean_data(synthetic_dataset)
    df_feat  = build_features(df_clean)
    feature_cols = get_feature_columns()
    X_train, X_test, y_train, y_test = split_train_test(df_feat, feature_cols)
    X_train_sc, X_test_sc, _ = normalize_features(X_train, X_test)
    return X_train_sc, X_test_sc, y_train, y_test


# ── Tests Preprocessing ───────────────────────────────────────────────────────

class TestPreprocessing:

    def test_generate_synthetic_data_shape(self, synthetic_dataset):
        assert synthetic_dataset.shape[0] > 700  # ~2 ans
        assert "consommation_mw" in synthetic_dataset.columns
        assert "temperature_moyenne" in synthetic_dataset.columns

    def test_generate_synthetic_data_no_nulls(self, synthetic_dataset):
        assert synthetic_dataset.isnull().sum().sum() == 0

    def test_clean_data_removes_duplicates(self, synthetic_dataset):
        df_dup = synthetic_dataset.append(synthetic_dataset.iloc[:5])
        df_clean = clean_data(df_dup)
        assert len(df_clean) == len(df_clean['date'].unique())

    def test_clean_data_no_nulls(self, synthetic_dataset):
        df_clean = clean_data(synthetic_dataset)
        assert df_clean.isnull().sum().sum() == 0

    def test_build_features_count(self, synthetic_dataset):
        df_clean = clean_data(synthetic_dataset)
        df_feat  = build_features(df_clean)
        feature_cols = get_feature_columns()
        assert len(feature_cols) == 14, f"Attendu 14 features, obtenu {len(feature_cols)}"

    def test_build_features_cyclical_encoding(self, synthetic_dataset):
        df_clean = clean_data(synthetic_dataset)
        df_feat  = build_features(df_clean)
        # Vérification que sin² + cos² ≈ 1 (encodage cyclique valide)
        sin_cos_sum = df_feat['mois_sin']**2 + df_feat['mois_cos']**2
        np.testing.assert_allclose(sin_cos_sum, 1.0, atol=1e-6)

    def test_split_temporal_order(self, synthetic_dataset):
        """Vérifie que le split respecte l'ordre temporel (pas de fuite du futur)."""
        df_clean = clean_data(synthetic_dataset)
        df_feat  = build_features(df_clean)
        feature_cols = get_feature_columns()
        X_train, X_test, y_train, y_test = split_train_test(df_feat, feature_cols)

        train_end_idx = int(len(df_feat) * 0.8) - 1
        # Les dates de train doivent précéder les dates de test
        assert df_feat['date'].iloc[train_end_idx] < df_feat['date'].iloc[train_end_idx + 1]

    def test_normalize_zero_mean(self, preprocessed_data):
        X_train_sc, _, _, _ = preprocessed_data
        np.testing.assert_allclose(X_train_sc.mean(axis=0), 0.0, atol=1e-6)

    def test_normalize_unit_std(self, preprocessed_data):
        X_train_sc, _, _, _ = preprocessed_data
        np.testing.assert_allclose(X_train_sc.std(axis=0), 1.0, atol=1e-6)


# ── Tests Métriques ───────────────────────────────────────────────────────────

class TestMetrics:

    def test_r2_perfect(self):
        y = np.array([1.0, 2.0, 3.0, 4.0])
        assert r2_score(y, y) == pytest.approx(1.0)

    def test_r2_baseline(self):
        y = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.full_like(y, y.mean())
        assert r2_score(y, y_pred) == pytest.approx(0.0, abs=1e-10)

    def test_rmse_perfect(self):
        y = np.array([100.0, 200.0, 300.0])
        assert rmse(y, y) == pytest.approx(0.0)

    def test_mape_perfect(self):
        y = np.array([100.0, 200.0, 300.0])
        assert mape(y, y) == pytest.approx(0.0)

    def test_mape_known_error(self):
        y_true = np.array([100.0])
        y_pred = np.array([110.0])
        assert mape(y_true, y_pred) == pytest.approx(10.0, rel=1e-3)

    def test_accuracy_within_tolerance(self):
        y_true = np.array([100.0, 200.0, 300.0])
        y_pred = np.array([105.0, 190.0, 295.0])  # tous dans ±10%
        assert accuracy_within_tolerance(y_true, y_pred, tolerance=0.10) == pytest.approx(100.0)

    def test_accuracy_partial(self):
        y_true = np.array([100.0, 100.0])
        y_pred = np.array([105.0, 120.0])  # 1 dans ±10%, 1 hors
        acc = accuracy_within_tolerance(y_true, y_pred, tolerance=0.10)
        assert acc == pytest.approx(50.0)


# ── Tests Modèles ─────────────────────────────────────────────────────────────

class TestRandomForest:

    def test_fit_predict(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        rf = RandomForestRegressor(n_estimators=10, random_state=42)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        assert y_pred.shape == y_test.shape

    def test_r2_positive(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        rf = RandomForestRegressor(n_estimators=10, random_state=42)
        rf.fit(X_train, y_train)
        assert r2_score(y_test, rf.predict(X_test)) > 0.5

    def test_no_negative_predictions(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        rf = RandomForestRegressor(n_estimators=10, random_state=42)
        rf.fit(X_train, y_train)
        assert (rf.predict(X_test) > 0).all()


class TestRBFNetwork:

    def test_init(self):
        rbf = RBFNetwork(n_centers=10, gamma=1.0, alpha=0.01)
        assert rbf.n_centers == 10
        assert rbf.gamma == 1.0

    def test_fit_sets_centers(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        rbf = RBFNetwork(n_centers=5, gamma=1.0, random_state=42)
        rbf.fit(X_train, y_train)
        assert rbf.centers_.shape == (5, X_train.shape[1])

    def test_predict_shape(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        rbf = RBFNetwork(n_centers=5, gamma=1.0, random_state=42)
        rbf.fit(X_train, y_train)
        y_pred = rbf.predict(X_test)
        assert y_pred.shape == (len(X_test),)

    def test_save_load(self, tmp_path, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        rbf = RBFNetwork(n_centers=5, gamma=1.0, random_state=42)
        rbf.fit(X_train, y_train)

        path = str(tmp_path / "rbf_test.pkl")
        rbf.save(path)
        rbf_loaded = RBFNetwork.load(path)

        np.testing.assert_array_almost_equal(
            rbf.predict(X_test),
            rbf_loaded.predict(X_test)
        )

    def test_rbf_activation_gaussian(self):
        rbf = RBFNetwork(n_centers=3, gamma=1.0)
        X       = np.zeros((1, 4))
        centers = np.eye(4)[:3]
        H = rbf._rbf_activation(X, centers)
        # Distance = 1.0 pour chaque centre → exp(-1.0 * 1) = exp(-1)
        np.testing.assert_allclose(H, np.exp(-1.0), atol=1e-6)


class TestDecisionTree:

    def test_fit_predict(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        dt = DecisionTreeRegressor(max_depth=5, random_state=42)
        dt.fit(X_train, y_train)
        y_pred = dt.predict(X_test)
        assert y_pred.shape == y_test.shape

    def test_depth_constraint(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        max_d = 5
        dt = DecisionTreeRegressor(max_depth=max_d, random_state=42)
        dt.fit(X_train, y_train)
        assert dt.get_depth() <= max_d


class TestKNN:

    def test_fit_predict(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        knn = KNeighborsRegressor(n_neighbors=5, weights='distance')
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        assert y_pred.shape == y_test.shape

    def test_r2_positive(self, preprocessed_data):
        X_train, X_test, y_train, y_test = preprocessed_data
        knn = KNeighborsRegressor(n_neighbors=5, weights='distance')
        knn.fit(X_train, y_train)
        assert r2_score(y_test, knn.predict(X_test)) > 0.0
