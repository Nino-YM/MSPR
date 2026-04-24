# Makefile — EDF Prediction Project
# Usage : make <target>

.PHONY: help install data train api test lint docker-up docker-down clean

help:  ## Affiche l'aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install:  ## Installe les dépendances Python
	pip install --upgrade pip
	pip install -r requirements.txt

data:  ## Génère et prétraite les données synthétiques
	cd notebooks && jupyter nbconvert --to notebook --execute 01_EDA_Exploration_Donnees.ipynb --inplace
	cd notebooks && jupyter nbconvert --to notebook --execute 02_Preprocessing_Feature_Engineering.ipynb --inplace

train:  ## Entraîne tous les modèles ML
	PYTHONPATH=src python -m models.train --model all

train-rf:  ## Entraîne uniquement Random Forest
	PYTHONPATH=src python -m models.train --model random_forest

api:  ## Lance l'API FastAPI en local (port 8000)
	PYTHONPATH=src uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

api-docs:  ## Ouvre la documentation Swagger
	start http://localhost:8000/docs

test:  ## Lance tous les tests unitaires
	pytest tests/unit/ -v --tb=short --cov=src --cov-report=term-missing

test-drift:  ## Lance les tests de drift detection
	pytest tests/unit/test_drift.py -v

lint:  ## Vérifie le style du code
	flake8 src --max-line-length=100 --exclude=__pycache__

docker-up:  ## Lance la stack Docker complète
	cd docker && docker compose --env-file .env.example up -d
	@echo "✅ Services démarrés :"
	@echo "   API      → http://localhost:8000"
	@echo "   Swagger  → http://localhost:8000/docs"
	@echo "   Grafana  → http://localhost:3000"
	@echo "   MLflow   → http://localhost:5000"
	@echo "   Prometheus → http://localhost:9090"

docker-down:  ## Arrête la stack Docker
	cd docker && docker compose down

docker-logs:  ## Affiche les logs de l'API
	cd docker && docker compose logs -f api

load-test:  ## Lance le test de charge Locust (interface web)
	locust -f tests/load/locustfile.py --host=http://localhost:8000

notebooks:  ## Lance Jupyter Lab
	jupyter lab notebooks/

clean:  ## Supprime les fichiers temporaires
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -f data/processed/*.npy data/processed/*.parquet data/processed/*.pkl 2>/dev/null || true
	rm -f data/models_saved/*.pkl data/models_saved/*.json 2>/dev/null || true
	@echo "✅ Nettoyage terminé"
