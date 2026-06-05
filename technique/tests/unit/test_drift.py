"""
Tests unitaires — Détection de dérive (drift detection)
pytest tests/unit/test_drift.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import numpy as np
import pytest
from monitoring.drift import ks_test_drift, psi_drift, cusum_drift, full_drift_analysis


@pytest.fixture
def stable_data():
    """Données sans dérive — même distribution."""
    rng = np.random.default_rng(42)
    X_ref = rng.normal(0, 1, (500, 14))
    X_cur = rng.normal(0, 1, (200, 14))
    return X_ref, X_cur


@pytest.fixture
def drifted_data():
    """Données avec dérive — distributions différentes."""
    rng = np.random.default_rng(42)
    X_ref = rng.normal(0, 1, (500, 14))
    X_cur = rng.normal(5, 2, (200, 14))  # Shift important
    return X_ref, X_cur


class TestKSTest:

    def test_no_drift_stable_data(self, stable_data):
        X_ref, X_cur = stable_data
        report = ks_test_drift(X_ref, X_cur)
        assert not report.drift_detected

    def test_drift_detected_different_distributions(self, drifted_data):
        X_ref, X_cur = drifted_data
        report = ks_test_drift(X_ref, X_cur)
        assert report.drift_detected

    def test_report_has_required_fields(self, stable_data):
        X_ref, X_cur = stable_data
        report = ks_test_drift(X_ref, X_cur)
        assert hasattr(report, "drift_detected")
        assert hasattr(report, "statistic")
        assert hasattr(report, "recommendation")
        assert 0.0 <= report.statistic <= 1.0

    def test_identical_data_no_drift(self):
        rng = np.random.default_rng(0)
        X = rng.normal(0, 1, (300, 14))
        report = ks_test_drift(X, X)
        assert not report.drift_detected


class TestPSI:

    def test_identical_predictions_no_drift(self):
        rng = np.random.default_rng(42)
        y_ref = rng.normal(60000, 5000, 500)
        report = psi_drift(y_ref, y_ref)
        assert not report.drift_detected
        assert report.statistic < 0.01

    def test_very_different_distributions_drift(self):
        rng = np.random.default_rng(42)
        y_ref = rng.normal(60000, 1000, 500)
        y_cur = rng.normal(40000, 1000, 200)  # Shift de 20 GW
        report = psi_drift(y_ref, y_cur)
        assert report.drift_detected

    def test_psi_non_negative(self):
        rng = np.random.default_rng(42)
        y_ref = rng.normal(60000, 5000, 500)
        y_cur = rng.normal(62000, 5500, 200)
        report = psi_drift(y_ref, y_cur)
        assert report.statistic >= 0


class TestCUSUM:

    def test_zero_mean_errors_no_drift(self):
        rng = np.random.default_rng(42)
        errors = rng.normal(0, 1000, 100)
        errors -= errors.mean()  # Force exact zero mean
        report = cusum_drift(errors)
        assert not report.drift_detected

    def test_biased_errors_drift_detected(self):
        rng = np.random.default_rng(42)
        # Biais systématique de +5000 MW
        errors = rng.normal(5000, 100, 100)
        report = cusum_drift(errors)
        assert report.drift_detected

    def test_statistic_is_positive(self):
        rng = np.random.default_rng(42)
        errors = rng.normal(0, 1000, 50)
        report = cusum_drift(errors)
        assert report.statistic >= 0


class TestFullAnalysis:

    def test_full_analysis_stable(self, stable_data):
        rng = np.random.default_rng(42)
        X_ref, X_cur = stable_data
        y_ref = rng.normal(60000, 5000, len(X_ref))
        # Subsample y_ref so PSI is guaranteed near 0 (same distribution by construction)
        y_cur = rng.choice(y_ref, size=len(X_cur), replace=False)
        errors = np.zeros(len(X_cur))  # Exact zero errors — CUSUM won't trigger

        report = full_drift_analysis(X_ref, X_cur, y_ref, y_cur, errors)
        assert "drift_detected" in report
        assert "n_alerts" in report
        assert "global_recommendation" in report
        assert report["n_alerts"] == 0
        assert not report["drift_detected"]

    def test_full_analysis_returns_dict(self, stable_data):
        rng = np.random.default_rng(42)
        X_ref, X_cur = stable_data
        y_ref = rng.normal(60000, 5000, 500)
        y_cur = rng.normal(60000, 5000, 200)
        errors = rng.normal(0, 500, 200)

        report = full_drift_analysis(X_ref, X_cur, y_ref, y_cur, errors)
        assert isinstance(report, dict)
        assert "ks_test" in report
        assert "psi" in report
        assert "cusum" in report
