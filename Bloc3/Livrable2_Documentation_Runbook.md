# DOCUMENTATION TECHNIQUE & RUNBOOK D'EXPLOITATION
## Projet EDF — Prédiction de la Consommation Électrique Journalière
### MSPR TPRE932 — Bloc de compétences 3 — Livrable 2

---

| Informations document | |
|---|---|
| **Version** | 1.0 |
| **Date** | Avril 2026 |
| **Auteurs** | A. Bernard (Data Scientist), C. Nguyen (DevOps) |
| **Validé par** | Y. Morin (Chef de projet) |
| **Audience** | Équipe technique, exploitants, nouveaux membres de l'équipe |

---

## TABLE DES MATIÈRES

1. Documentation technique des modèles IA
2. Description des scripts et services de déploiement
3. Pré-requis techniques
4. Runbook / Guide d'exploitation
5. Note d'expertise technique à l'équipe projet

---

## 1. DOCUMENTATION TECHNIQUE DES MODÈLES IA

### 1.1 Contexte général

Quatre algorithmes de Machine Learning ont été implémentés pour la prédiction de la consommation électrique journalière des abonnés EDF. Chaque modèle reçoit les mêmes variables d'entrée et produit la même sortie, permettant une comparaison objective de leurs performances.

#### Variables d'entrée (features)

| Variable | Type | Description | Source |
|---|---|---|---|
| `consommation_j1` | Float (MW) | Consommation réelle de la veille | RTE éco2mix |
| `consommation_j7` | Float (MW) | Consommation réelle il y a 7 jours (même jour de la semaine) | RTE éco2mix |
| `temperature_moyenne` | Float (°C) | Température moyenne journalière nationale | Météo France |
| `temperature_min` | Float (°C) | Température minimale journalière | Météo France |
| `temperature_max` | Float (°C) | Température maximale journalière | Météo France |
| `type_jour` | Catégoriel | 0=jour ouvré, 1=week-end, 2=jour férié | Calendrier EDF |
| `mois` | Entier (1-12) | Mois de l'année (saisonnalité) | Calculé |
| `jour_semaine` | Entier (0-6) | Jour de la semaine (lundi=0) | Calculé |

#### Variable de sortie (cible)

| Variable | Type | Description |
|---|---|---|
| `consommation_j` | Float (MW) | Consommation électrique totale journalière nationale prédite |

#### Prétraitement des données

```
Étape 1 — Collecte : API RTE éco2mix (format JSON) → DataFrame Pandas
Étape 2 — Nettoyage :
  - Valeurs manquantes : interpolation linéaire (si < 3 valeurs consécutives manquantes)
  - Outliers : détection IQR, remplacement par la médiane glissante sur 7 jours
  - Doublons : suppression
Étape 3 — Encodage : variable type_jour → One-Hot Encoding (3 colonnes)
Étape 4 — Normalisation : StandardScaler (moyenne=0, écart-type=1) sur les variables numériques
Étape 5 — Split train/test : 80 % entraînement (2019-2022) / 20 % test (2023-2024)
```

---

### 1.2 Modèle 1 — Réseau de Neurones RBF (Radial Basis Function)

#### Description

Le réseau de neurones à fonctions de base radiales (RBF) est un réseau à propagation avant à 3 couches, dont la couche cachée utilise des fonctions gaussiennes comme fonctions d'activation. Il est particulièrement adapté aux problèmes de régression non linéaires avec des données temporelles.

#### Architecture

```
Couche d'entrée : 10 neurones (8 features + 2 variables encodées One-Hot)
        │
        ▼
Couche cachée RBF : 50 neurones
  - Fonction d'activation : Gaussienne φ(x) = exp(-||x-c||² / 2σ²)
  - Centres (c) : déterminés par K-Means clustering sur le dataset d'entraînement
  - Largeur (σ) : optimisée par validation croisée 5-fold
        │
        ▼
Couche de sortie : 1 neurone (consommation prédite en MW)
  - Activation : linéaire
  - Optimiseur : SGD avec momentum (lr=0,01, momentum=0,9)
```

#### Hyperparamètres principaux

| Hyperparamètre | Valeur | Justification |
|---|---|---|
| Nombre de neurones RBF | 50 | Optimal par GridSearchCV (testé 20, 50, 100) |
| Taux d'apprentissage | 0,01 | Convergence stable sans oscillation |
| Epochs d'entraînement | 200 | Early stopping après 20 epochs sans amélioration |
| Batch size | 32 | Compromis vitesse/stabilité |
| Régularisation L2 | 0,001 | Prévention du sur-apprentissage |

#### Métriques de performance (dataset test 2023-2024)

| Métrique | Valeur |
|---|---|
| **R² Score** | 0,94 |
| **RMSE** | 312 MW |
| **MAPE** | 3,9 % |
| **Accuracy (±10 %)** | 96,2 % |
| **Temps d'entraînement (5 ans de données)** | 18 min |
| **Temps d'inférence (1 prédiction)** | 45 ms |

---

### 1.3 Modèle 2 — Forêt Aléatoire (Random Forest)

#### Description

La forêt aléatoire est un ensemble de N arbres de décision entraînés sur des sous-échantillons aléatoires du dataset (bagging). La prédiction finale est la moyenne des prédictions de chaque arbre. Ce modèle est robuste aux outliers et offre une excellente interprétabilité via l'importance des variables.

#### Hyperparamètres principaux

| Hyperparamètre | Valeur | Justification |
|---|---|---|
| `n_estimators` | 200 | Compromis performance/temps de calcul (testé 100, 200, 500) |
| `max_depth` | 15 | Prévention du sur-apprentissage (profondeur illimitée → overfitting) |
| `min_samples_split` | 10 | Évite les nœuds trop spécifiques |
| `min_samples_leaf` | 5 | Stabilité des feuilles terminales |
| `max_features` | `sqrt` | Standard pour la régression : √(nb_features) |
| `bootstrap` | True | Activation du bagging |
| `random_state` | 42 | Reproductibilité des résultats |

#### Importance des variables (feature importance)

| Rang | Variable | Importance relative |
|---|---|---|
| 1 | `consommation_j1` | 38,2 % |
| 2 | `temperature_moyenne` | 24,7 % |
| 3 | `consommation_j7` | 18,1 % |
| 4 | `mois` | 9,3 % |
| 5 | `temperature_min` | 4,8 % |
| 6 | `type_jour` | 3,6 % |
| 7 | `temperature_max` | 0,9 % |
| 8 | `jour_semaine` | 0,4 % |

**Interprétation :** La consommation de la veille et la température sont les deux facteurs les plus prédictifs. C'est cohérent avec le comportement réel du réseau électrique français, où le chauffage électrique représente environ 30 % de la consommation nationale.

#### Métriques de performance (dataset test 2023-2024)

| Métrique | Valeur |
|---|---|
| **R² Score** | **0,95** ← Meilleur modèle |
| **RMSE** | **274 MW** ← Meilleur modèle |
| **MAPE** | **3,6 %** ← Meilleur modèle |
| **Accuracy (±10 %)** | **97,1 %** |
| **Temps d'entraînement (5 ans de données)** | 8 min |
| **Temps d'inférence (1 prédiction)** | 12 ms |

---

### 1.4 Modèle 3 — Arbre de Décision

#### Description

L'arbre de décision est un modèle hiérarchique qui partitionne récursivement l'espace des features pour minimiser l'erreur de prédiction. Il offre une excellente interprétabilité (on peut visualiser l'arbre entier) mais est plus sensible au sur-apprentissage que la forêt aléatoire.

#### Hyperparamètres principaux

| Hyperparamètre | Valeur | Justification |
|---|---|---|
| `max_depth` | 8 | Limiter la profondeur pour réduire l'overfitting |
| `min_samples_split` | 20 | Nœud minimum pour une division |
| `min_samples_leaf` | 10 | Feuille minimum pour la stabilité |
| `criterion` | `squared_error` | Standard pour la régression |
| `random_state` | 42 | Reproductibilité |

#### Métriques de performance (dataset test 2023-2024)

| Métrique | Valeur |
|---|---|
| **R² Score** | 0,87 |
| **RMSE** | 498 MW |
| **MAPE** | 6,5 % |
| **Accuracy (±10 %)** | 89,4 % |
| **Temps d'entraînement (5 ans de données)** | 45 s |
| **Temps d'inférence (1 prédiction)** | 3 ms |

**Note :** L'arbre de décision présente des performances inférieures mais offre l'avantage d'être entièrement interprétable — utile pour justifier les prédictions aux opérateurs EDF non-techniciens.

---

### 1.5 Modèle 4 — K-Nearest Neighbors (KNN)

#### Description

L'algorithme KNN prédit la consommation d'une journée donnée en identifiant les K journées historiques les plus similaires (selon la distance euclidienne dans l'espace des features normalisées) et en calculant la moyenne de leurs consommations réelles.

#### Hyperparamètres principaux

| Hyperparamètre | Valeur | Justification |
|---|---|---|
| `n_neighbors` | 7 | Optimal par validation croisée 5-fold (testé 3, 5, 7, 10, 15) |
| `metric` | `euclidean` | Distance standard adaptée aux données normalisées |
| `weights` | `distance` | Les voisins les plus proches ont un poids plus important |
| `algorithm` | `ball_tree` | Plus efficace pour un nombre modéré de features |

#### Métriques de performance (dataset test 2023-2024)

| Métrique | Valeur |
|---|---|
| **R² Score** | 0,91 |
| **RMSE** | 421 MW |
| **MAPE** | 4,9 % |
| **Accuracy (±10 %)** | 93,7 % |
| **Temps d'entraînement (5 ans de données)** | 0 s (pas d'entraînement, mémorisation) |
| **Temps d'inférence (1 prédiction)** | 280 ms (recherche des K voisins) |

**Note :** Le temps d'inférence élevé du KNN (280 ms) le disqualifie pour une utilisation en production à haute fréquence. Il est conservé à titre comparatif et pour des analyses ponctuelles.

---

### 1.6 Tableau comparatif des modèles

| Modèle | R² | RMSE (MW) | MAPE | Accuracy ±10% | Tps inférence | Rôle en production |
|---|---|---|---|---|---|---|
| Forêt Aléatoire | **0,95** | **274** | **3,6 %** | **97,1 %** | 12 ms | **Modèle principal** |
| Réseau de neurones RBF | 0,94 | 312 | 3,9 % | 96,2 % | 45 ms | Modèle de validation |
| KNN | 0,91 | 421 | 4,9 % | 93,7 % | 280 ms | Analyse ponctuelle |
| Arbre de Décision | 0,87 | 498 | 6,5 % | 89,4 % | 3 ms | Modèle explicatif |

---

## 2. DESCRIPTION DES SCRIPTS ET SERVICES DE DÉPLOIEMENT

### 2.1 Structure du projet

```
edf-prediction/
├── data/
│   ├── raw/                    # Données brutes RTE éco2mix
│   ├── processed/              # Données prétraitées
│   └── models/                 # Modèles sérialisés (.pkl, .h5)
├── src/
│   ├── data_pipeline/
│   │   ├── ingestion.py        # Collecte API RTE éco2mix
│   │   ├── preprocessing.py    # Nettoyage et normalisation
│   │   └── feature_eng.py      # Feature engineering
│   ├── models/
│   │   ├── train.py            # Entraînement de tous les modèles
│   │   ├── evaluate.py         # Calcul des métriques
│   │   └── predict.py          # Inférence
│   └── api/
│       ├── main.py             # Application FastAPI
│       ├── schemas.py          # Modèles Pydantic (validation des données)
│       ├── auth.py             # Authentification JWT
│       └── monitoring.py       # Expositions Prometheus
├── tests/
│   ├── unit/                   # Tests unitaires (pytest)
│   ├── integration/            # Tests d'intégration
│   └── load/                   # Scripts Locust (tests de charge)
├── docker/
│   ├── Dockerfile              # Image API
│   ├── Dockerfile.dashboard    # Image Streamlit
│   └── docker-compose.yml      # Orchestration locale
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Pipeline GitHub Actions
├── mlflow/
│   └── experiments/            # Logs MLflow
├── monitoring/
│   ├── prometheus.yml          # Configuration Prometheus
│   └── grafana/
│       └── dashboards/         # JSON des dashboards Grafana
└── requirements.txt
```

### 2.2 Dockerfile — Service API

```dockerfile
# Dockerfile — edf-prediction API
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="equipe-mspr-edf@example.com"
LABEL version="1.0"
LABEL description="API FastAPI de prédiction de consommation électrique EDF"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    PORT=8000

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code applicatif
COPY src/api/ ./api/
COPY data/models/ ./models/

# Utilisateur non-root (sécurité)
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Exposition du port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Commande de démarrage
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 2.3 API FastAPI — Endpoints principaux

```python
# src/api/main.py (extrait simplifié)

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import joblib, numpy as np

app = FastAPI(
    title="EDF Electricity Prediction API",
    description="Prédiction de la consommation électrique journalière nationale",
    version="1.0.0"
)

# --- Schémas de données ---
class PredictionInput(BaseModel):
    consommation_j1: float = Field(..., gt=0, description="Consommation veille (MW)")
    consommation_j7: float = Field(..., gt=0, description="Consommation J-7 (MW)")
    temperature_moyenne: float = Field(..., ge=-30, le=50, description="Température moyenne (°C)")
    temperature_min: float = Field(..., ge=-30, le=50)
    temperature_max: float = Field(..., ge=-30, le=50)
    type_jour: int = Field(..., ge=0, le=2, description="0=ouvré, 1=week-end, 2=férié")
    mois: int = Field(..., ge=1, le=12)
    jour_semaine: int = Field(..., ge=0, le=6)

class PredictionOutput(BaseModel):
    prediction_mw: float
    modele_utilise: str
    r2_score: float
    mape: float
    timestamp: str

# --- Endpoints ---
@app.get("/health")
def health_check():
    """Vérification de la disponibilité du service."""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, token: str = Depends(verify_jwt)):
    """Génère une prédiction de consommation électrique journalière."""
    features = preprocess_input(data)
    prediction = model_rf.predict(features)[0]
    return PredictionOutput(
        prediction_mw=round(prediction, 2),
        modele_utilise="random_forest_v1.2",
        r2_score=0.95,
        mape=3.6,
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/metrics")
def get_metrics():
    """Expose les métriques Prometheus."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### 2.4 Pipeline CI/CD — GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
name: EDF Prediction — CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # --- ÉTAPE 1 : Tests et qualité de code ---
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run linting (flake8)
        run: flake8 src/ --max-line-length=120
      - name: Run unit tests (pytest)
        run: pytest tests/unit/ -v --cov=src --cov-report=xml
      - name: Run integration tests
        run: pytest tests/integration/ -v

  # --- ÉTAPE 2 : Build de l'image Docker ---
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-3
      - name: Login to AWS ECR
        run: aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
      - name: Build and push Docker image
        run: |
          docker build -t edf-api:${{ github.sha }} -f docker/Dockerfile .
          docker tag edf-api:${{ github.sha }} $ECR_REGISTRY/edf-api:${{ github.sha }}
          docker push $ECR_REGISTRY/edf-api:${{ github.sha }}
          docker tag edf-api:${{ github.sha }} $ECR_REGISTRY/edf-api:latest
          docker push $ECR_REGISTRY/edf-api:latest

  # --- ÉTAPE 3 : Déploiement en production ---
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to AWS EC2 via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/edf-prediction
            docker pull $ECR_REGISTRY/edf-api:latest
            docker-compose up -d --no-deps edf-api
            docker system prune -f
```

---

## 3. PRÉ-REQUIS TECHNIQUES

### 3.1 Ressources minimales recommandées

| Environnement | CPU | RAM | Stockage | OS |
|---|---|---|---|---|
| **Développement** | 4 vCPU | 8 Go | 50 Go SSD | Ubuntu 22.04 / macOS 13+ / Windows 11 |
| **Test / Staging** | 2 vCPU | 4 Go | 30 Go SSD | Ubuntu 22.04 |
| **Production** | 4 vCPU | 8 Go | 100 Go SSD | Ubuntu 22.04 |

### 3.2 Logiciels et versions

| Logiciel | Version | Rôle |
|---|---|---|
| **Python** | 3.11.x | Langage principal |
| **Docker** | 24.x | Conteneurisation |
| **Docker Compose** | 2.x | Orchestration locale |
| **Git** | 2.x | Versioning du code |
| **FastAPI** | 0.110.x | Framework API REST |
| **Uvicorn** | 0.29.x | Serveur ASGI |
| **scikit-learn** | 1.4.x | Modèles ML |
| **TensorFlow / Keras** | 2.15.x | Réseau de neurones RBF |
| **Pandas** | 2.2.x | Manipulation des données |
| **NumPy** | 1.26.x | Calcul numérique |
| **MLflow** | 2.11.x | Tracking des modèles |
| **Prometheus Client** | 0.20.x | Monitoring |
| **PostgreSQL** | 15.x | Base de données |
| **Locust** | 2.x | Tests de charge |

### 3.3 Variables d'environnement requises

| Variable | Exemple | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/edf_db` | Connexion PostgreSQL |
| `JWT_SECRET_KEY` | `[clé aléatoire 256 bits]` | Secret pour les tokens JWT |
| `RTE_API_KEY` | `[clé API RTE]` | Accès à l'API éco2mix |
| `MLFLOW_TRACKING_URI` | `http://mlflow:5000` | URL du serveur MLflow |
| `AWS_S3_BUCKET` | `edf-prediction-models` | Bucket S3 pour les modèles |
| `APP_ENV` | `production` | Environnement actif |
| `LOG_LEVEL` | `INFO` | Niveau de logs |

**Sécurité :** Ces variables ne doivent jamais être committées dans Git. Utiliser AWS Secrets Manager en production et un fichier `.env` (dans `.gitignore`) en développement.

---

## 4. RUNBOOK / GUIDE D'EXPLOITATION

### 4.1 Démarrer la solution

#### En développement (local)
```bash
# Cloner le dépôt
git clone https://github.com/edf/edf-prediction.git
cd edf-prediction

# Copier les variables d'environnement
cp .env.example .env
# Éditer .env avec les valeurs locales

# Démarrer tous les services
docker-compose up -d

# Vérifier que tous les services sont actifs
docker-compose ps

# Tester l'API
curl http://localhost:8000/health
```

#### En production (AWS)
```bash
# Connexion au serveur EC2
ssh -i edf-keypair.pem ubuntu@<IP_EC2>

# Naviguer vers le répertoire de l'application
cd /opt/edf-prediction

# Démarrer les services
docker-compose -f docker-compose.prod.yml up -d

# Vérifier l'état
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f edf-api
```

**Temps de démarrage estimé :** 45 à 90 secondes selon la disponibilité des modèles en S3.

### 4.2 Arrêter la solution

```bash
# Arrêt propre (les requêtes en cours sont terminées)
docker-compose -f docker-compose.prod.yml stop

# Arrêt et suppression des conteneurs (les données sont conservées dans les volumes)
docker-compose -f docker-compose.prod.yml down

# Arrêt d'urgence (si le conteneur ne répond plus)
docker kill edf-api
docker-compose -f docker-compose.prod.yml down
```

### 4.3 Déployer une nouvelle version de modèle

```bash
# Étape 1 : Déclencher le ré-entraînement
python src/models/train.py --dataset data/processed/latest.parquet

# Étape 2 : Évaluer le nouveau modèle
python src/models/evaluate.py --model models/random_forest_new.pkl

# Étape 3 : Si les métriques sont meilleures, enregistrer dans MLflow
python src/models/register.py --model models/random_forest_new.pkl --name "random_forest_v1.3"

# Étape 4 : Construire la nouvelle image Docker
docker build -t edf-api:v1.3 -f docker/Dockerfile .

# Étape 5 : Pousser vers AWS ECR
docker push $ECR_REGISTRY/edf-api:v1.3

# Étape 6 : Mise à jour en production (Blue/Green)
# Modifier le tag dans docker-compose.prod.yml
sed -i 's/edf-api:v1.2/edf-api:v1.3/g' docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d --no-deps edf-api

# Étape 7 : Vérification post-déploiement
curl http://localhost:8000/health
curl http://localhost:8000/metrics | grep r2_score
```

### 4.4 Procédure de rollback (retour en arrière)

À utiliser en cas de dégradation des performances après un déploiement.

```bash
# Étape 1 : Identifier la version précédente stable
docker images | grep edf-api

# Étape 2 : Revenir à la version précédente
docker-compose -f docker-compose.prod.yml stop edf-api
sed -i 's/edf-api:v1.3/edf-api:v1.2/g' docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d edf-api

# Étape 3 : Vérifier que le service est restauré
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"consommation_j1": 45000, "temperature_moyenne": 12.5, ...}'

# Étape 4 : Notifier l'équipe projet
# → Email automatique envoyé par le script de monitoring
# → Ticket d'incident créé dans le backlog

# Étape 5 : Annuler le modèle dans MLflow
mlflow models set-model-version-tag --name "random_forest" --version 3 --key "status" --value "failed"
```

**Durée de rollback estimée :** 2 à 5 minutes.

### 4.5 Vérifications essentielles (health checks)

Effectuer ces vérifications à chaque démarrage et après chaque déploiement :

| Vérification | Commande | Résultat attendu |
|---|---|---|
| API disponible | `curl http://host:8000/health` | `{"status": "healthy"}` |
| Prédiction fonctionnelle | `curl -X POST /predict -d {...}` | JSON avec `prediction_mw` > 0 |
| Base de données accessible | `docker exec edf-db psql -U edf -c "\l"` | Liste des bases visible |
| Modèle chargé | `curl /metrics \| grep model_loaded` | `model_loaded 1` |
| Monitoring actif | `curl http://host:9090/graph` | Interface Prometheus accessible |
| Dashboard Grafana | `curl http://host:3000/api/health` | `{"database": "ok"}` |

### 4.6 Procédure de gestion des incidents

#### Arbre de décision — Incidents courants

**Incident 1 : L'API ne répond plus (timeout ou HTTP 503)**
```
Symptôme : curl /health retourne une erreur
    │
    ▼
1. Vérifier les logs : docker logs edf-api --tail 100
    │
    ├── OOM Kill → Augmenter la RAM du conteneur / redémarrer
    ├── Erreur DB → Vérifier la connexion PostgreSQL (cf. Incident 2)
    ├── Crash Python → Analyser la stack trace, patch + redéploiement
    └── Conteneur arrêté → docker-compose up -d edf-api
```

**Incident 2 : Performances des prédictions dégradées (MAPE > 5 %)**
```
Symptôme : Alerte Grafana — MAPE > 5 % pendant 3 jours
    │
    ▼
1. Vérifier si les données RTE éco2mix sont correctement ingérées
    │
    ├── Données manquantes → Relancer l'ingestion manuellement
    ├── Data drift détecté → Déclencher ré-entraînement (cf. 4.3)
    └── Bug de prétraitement → Analyser le pipeline preprocessing.py
```

**Incident 3 : Données entrantes dans un format inattendu**
```
Symptôme : HTTP 422 Unprocessable Entity en masse dans les logs
    │
    ▼
1. Analyser un payload d'exemple : docker logs edf-api | grep 422
2. Identifier le champ mal formaté (ex : unité en kW au lieu de MW)
3. Mise à jour du schéma Pydantic ou communication aux appelants
```

#### Niveaux de priorité des incidents

| Niveau | Critère | Délai de résolution | Escalade |
|---|---|---|---|
| **P1 — Critique** | API indisponible en production | < 1 heure | Chef de projet + DSI EDF immédiatement |
| **P2 — Majeur** | MAPE > 10 % pendant 24h | < 4 heures | Chef de projet + Data Scientist |
| **P3 — Modéré** | Performance dégradée (MAPE 5-10 %) | < 24 heures | Data Scientist + DevOps |
| **P4 — Mineur** | Anomalie non bloquante | < 72 heures | Équipe projet |

---

## 5. NOTE D'EXPERTISE TECHNIQUE À L'ÉQUIPE PROJET

### 5.1 Choix techniques clés pour le déploiement et la maintenabilité

#### Pourquoi la Forêt Aléatoire comme modèle principal ?

Bien que le réseau de neurones RBF offre des performances légèrement inférieures, il est **beaucoup moins stable** en production pour les raisons suivantes :
- **Sensibilité aux données d'entrée :** un outlier dans les données de température peut faire diverger les prédictions.
- **Temps d'entraînement :** 18 minutes vs 8 minutes pour la Random Forest lors d'un ré-entraînement.
- **Interprétabilité :** impossible d'expliquer une prédiction RBF à un opérateur EDF non-technique.

La Forêt Aléatoire offre le **meilleur ratio performance / robustesse / maintenabilité** pour un environnement de production.

#### Pourquoi FastAPI plutôt que Flask ou Django ?

FastAPI offre :
- **Validation automatique des données** via Pydantic (protection contre les injections de données malformées)
- **Documentation API auto-générée** (Swagger UI à `/docs`) — précieux pour l'équipe EDF
- **Performance supérieure** (framework asynchrone basé sur Starlette)
- **Support natif des types Python** — code plus lisible et maintenable

#### Pourquoi MLflow pour le tracking des modèles ?

Sans MLflow, les équipes perdent rapidement la traçabilité des expériences : "Quel modèle était en prod en janvier ? Avec quels hyperparamètres ?" MLflow garantit :
- La **reproductibilité** : on peut re-créer n'importe quelle version d'un modèle
- La **comparaison objective** : toutes les métriques sont centralisées
- Le **déploiement tracé** : on sait exactement quel modèle a été déployé et quand

### 5.2 Bonnes pratiques — Recommandations à l'équipe

#### Sécurité et gestion des secrets
- **Ne jamais stocker de secrets en clair** dans le code ou les fichiers de configuration. Utiliser AWS Secrets Manager en production.
- **Authentification JWT** sur tous les endpoints sensibles — renouvellement des tokens toutes les 24h.
- **Données personnelles :** la solution travaille sur des données agrégées nationales. Si des données individuelles devaient être intégrées, une analyse d'impact RGPD (AIPD) est obligatoire avant tout traitement.

#### Qualité du code
- **Écrire des tests unitaires** pour chaque fonction de preprocessing et chaque endpoint API. Objectif : couverture de code ≥ 80 %.
- **Documenter les fonctions** avec des docstrings clairs (paramètres, valeurs de retour, exceptions possibles).
- **Linting systématique** avec flake8 avant chaque commit (intégré au pre-commit hook Git).

#### Logs
- **Structurer les logs en JSON** (format compatible ELK Stack) pour faciliter l'analyse.
- **Niveau INFO minimum** en production — DEBUG uniquement sur les environnements de développement.
- **Ne jamais logger de données sensibles** (clés API, tokens JWT, données utilisateurs).
- Exemple de log structuré :
```json
{
  "timestamp": "2026-04-24T14:23:11Z",
  "level": "INFO",
  "service": "edf-api",
  "endpoint": "/predict",
  "duration_ms": 187,
  "prediction_mw": 48234.5,
  "model_version": "random_forest_v1.2"
}
```

#### Concept DIC (Disponibilité — Intégrité — Confidentialité)

| Pilier | Mesures implémentées |
|---|---|
| **Disponibilité** | Load Balancer AWS, multi-instances, monitoring 24/7, procédure de rollback < 5 min |
| **Intégrité** | Validation Pydantic de tous les inputs, checksums MD5 des modèles sérialisés, versioning Git + MLflow |
| **Confidentialité** | HTTPS obligatoire (TLS 1.3), authentification JWT, pas de données personnelles, accès restreint par rôle (RBAC) |

#### Éléments essentiels du RGPD applicables au projet

- **Article 25 — Privacy by Design :** la solution a été conçue dès le départ pour ne traiter que des données agrégées (consommation nationale), sans aucune donnée personnelle identifiable.
- **Article 32 — Sécurité :** chiffrement des données en transit (HTTPS/TLS) et au repos (chiffrement AWS S3 + RDS).
- **Article 30 — Registre des traitements :** ce projet doit être déclaré dans le registre des traitements de la DPO d'EDF.
- **Article 35 — AIPD :** une Analyse d'Impact sur la Protection des Données est requise si le projet évolue vers le traitement de données de consommation individuelles par compteur Linky.

---

*Document rédigé par l'équipe projet MSPR EDF — Avril 2026*
*Référence : MSPR-TPRE932-B3-L2-v1.0*
