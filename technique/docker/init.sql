-- Initialisation de la base de données EDF Predictions

-- Table des prédictions
CREATE TABLE IF NOT EXISTS predictions (
    id              SERIAL PRIMARY KEY,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_prediction DATE NOT NULL,
    model_used      VARCHAR(50) NOT NULL,
    temperature_moy FLOAT NOT NULL,
    type_jour       SMALLINT NOT NULL CHECK (type_jour IN (0, 1, 2)),
    consommation_mw FLOAT NOT NULL,
    inference_ms    FLOAT,
    user_id         VARCHAR(100)
);

-- Table des métriques de dérive
CREATE TABLE IF NOT EXISTS drift_metrics (
    id          SERIAL PRIMARY KEY,
    computed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    model_name  VARCHAR(50) NOT NULL,
    mape_7d     FLOAT,
    r2_7d       FLOAT,
    ks_statistic FLOAT,
    drift_detected BOOLEAN DEFAULT FALSE
);

-- Index pour les requêtes fréquentes
CREATE INDEX IF NOT EXISTS idx_predictions_date ON predictions(date_prediction);
CREATE INDEX IF NOT EXISTS idx_predictions_model ON predictions(model_used);
CREATE INDEX IF NOT EXISTS idx_drift_model ON drift_metrics(model_name);

-- Vue pour les métriques journalières
CREATE OR REPLACE VIEW daily_metrics AS
SELECT
    date_prediction,
    model_used,
    COUNT(*) AS nb_predictions,
    AVG(inference_ms) AS avg_inference_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY inference_ms) AS p95_inference_ms
FROM predictions
GROUP BY date_prediction, model_used
ORDER BY date_prediction DESC;

COMMENT ON TABLE predictions IS 'Historique des prédictions de consommation électrique EDF';
COMMENT ON TABLE drift_metrics IS 'Métriques de dérive du modèle ML en production';
