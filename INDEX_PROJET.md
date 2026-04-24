# INDEX DU PROJET MSPR — EDF IA PREDICT
## Certification Chef de Projet Expert en Intelligence Artificielle — RNCP 36582
### EPSI — Niveau 7

---

## INFORMATIONS GÉNÉRALES

| | |
|---|---|
| **Sujet** | Déploiement d'une solution IA basée sur la prédiction de la consommation électrique pour EDF |
| **Entreprise cliente** | EDF (Électricité de France) — Direction R&D |
| **Équipe** | 4 apprenants |
| **Durée de préparation** | 38 heures |
| **Soutenances** | 2 soutenances de 50 min chacune (20 min présentation + 30 min jury) |

---

## STRUCTURE DES LIVRABLES

### BLOC 3 — Préparer la maintenabilité et le déploiement de la solution I.A (TPRE932)

| # | Livrable | Fichier | Contenu |
|---|---|---|---|
| 1 | Dossier de déploiement & maintenabilité | [Bloc3/Livrable1_Deploiement_Maintenabilite.md](Bloc3/Livrable1_Deploiement_Maintenabilite.md) | Architecture (schéma data→modèles→API→users), processus de maintenabilité, test de déploiement par simulation virtuelle (4 scénarios) |
| 2 | Documentation technique & runbook d'exploitation | [Bloc3/Livrable2_Documentation_Runbook.md](Bloc3/Livrable2_Documentation_Runbook.md) | Documentation des 4 modèles ML (RBF, RF, DT, KNN), Dockerfile, API FastAPI, CI/CD, runbook complet (start/stop/rollback/incidents), note d'expertise DIC + RGPD |
| 3 | Plan d'accompagnement du changement | [Bloc3/Livrable3_Accompagnement_Changement.md](Bloc3/Livrable3_Accompagnement_Changement.md) | Analyse d'impact (parties prenantes, processus), stratégie ADKAR (5 phases), kit Lean management (formulaire feedback, tableau A3, réunion amélioration continue) |

### BLOC 4 — Manager un projet informatique avec Agilité (TPRE942)

| # | Livrable | Fichier | Contenu |
|---|---|---|---|
| 1 | Dossier de cadrage & cahier des charges | [Bloc4/Livrable1_Cadrage_Cahier_Charges.md](Bloc4/Livrable1_Cadrage_Cahier_Charges.md) | Objectifs métier & techniques, WBS, Gantt (8 semaines, 4 sprints), budget 130 K€, CDC fonctionnel (user stories, règles de gestion, KPI, dates clés), CDC technique, PERT avec chemin critique |
| 2 | Dossier de pilotage agile & suivi | [Bloc4/Livrable2_Pilotage_Agile.md](Bloc4/Livrable2_Pilotage_Agile.md) | Méthode Scrum (justification), rôles, cérémonies (Daily, Review, Retro), backlog priorisé MoSCoW (22 US / 128 SP), Burndown Chart, tableaux de bord sponsor + chef de projet, pilotage prestataires (SLA, RACI, pénalités) |
| 3 | Plan d'inclusion, communication & collaboration | [Bloc4/Livrable3_Inclusion_Communication.md](Bloc4/Livrable3_Inclusion_Communication.md) | 6 familles AGEFIPH (adaptations concrètes), communication interculturelle (5 pays EDF, modèle Hofstede), 4 solutions innovantes (serious game, café virtuel, webinaires), kit réunion à distance (Teams, Klaxoon, Kahoot, Padlet) |

---

## IMPLÉMENTATION TECHNIQUE

### Notebooks Jupyter — Analyse & Modélisation

| # | Notebook | Contenu |
|---|---|---|
| 01 | [technique/notebooks/01_EDA_Exploration_Donnees.ipynb](technique/notebooks/01_EDA_Exploration_Donnees.ipynb) | EDA : saisonnalité, thermosensibilité, corrélations, outliers |
| 02 | [technique/notebooks/02_Preprocessing_Feature_Engineering.ipynb](technique/notebooks/02_Preprocessing_Feature_Engineering.ipynb) | Pipeline preprocessing : lag features, encodage cyclique, split temporel, StandardScaler |
| 03 | [technique/notebooks/03_Modele_Random_Forest.ipynb](technique/notebooks/03_Modele_Random_Forest.ipynb) | Random Forest : GridSearchCV, feature importance, analyse residus |
| 04 | [technique/notebooks/04_Modele_RBF_Neural_Network.ipynb](technique/notebooks/04_Modele_RBF_Neural_Network.ipynb) | Réseau RBF custom : optimisation gamma/n_centers, visualisation K-Means |
| 05 | [technique/notebooks/05_Modele_Arbre_Decision.ipynb](technique/notebooks/05_Modele_Arbre_Decision.ipynb) | Arbre de Décision : courbe validation, visualisation arbre, extraction de règles |
| 06 | [technique/notebooks/06_Modele_KNN.ipynb](technique/notebooks/06_Modele_KNN.ipynb) | KNN : optimisation K, analyse temps d'inférence, discussion production |
| 07 | [technique/notebooks/07_Comparaison_Modeles.ipynb](technique/notebooks/07_Comparaison_Modeles.ipynb) | Comparaison finale : radar chart, score pondéré EDF, sélection Random Forest |
| 08 | [technique/notebooks/08_Monitoring_Production.ipynb](technique/notebooks/08_Monitoring_Production.ipynb) | Monitoring & drift detection : KS Test, PSI, CUSUM — simulation scénario COVID |

### Code Source

| Fichier | Rôle |
|---|---|
| [technique/src/data_pipeline/ingestion.py](technique/src/data_pipeline/ingestion.py) | Chargement données RTE + génération synthétique |
| [technique/src/data_pipeline/preprocessing.py](technique/src/data_pipeline/preprocessing.py) | Pipeline complet : nettoyage, features, split, normalisation |
| [technique/src/models/rbf_network.py](technique/src/models/rbf_network.py) | Réseau RBF from scratch (compatible scikit-learn) |
| [technique/src/models/evaluate.py](technique/src/models/evaluate.py) | Métriques : R², RMSE, MAPE, accuracy, inference time |
| [technique/src/models/train.py](technique/src/models/train.py) | CLI d'entraînement de tous les modèles |
| [technique/src/api/main.py](technique/src/api/main.py) | API FastAPI : /predict, /health, /metrics, /models |
| [technique/src/api/auth.py](technique/src/api/auth.py) | Authentification JWT (rôles reader/analyst/admin) |
| [technique/src/api/schemas.py](technique/src/api/schemas.py) | Schémas Pydantic entrée/sortie |

### Infrastructure & DevOps

| Fichier | Rôle |
|---|---|
| [technique/docker/Dockerfile](technique/docker/Dockerfile) | Image Docker multi-stage (python:3.10-slim) |
| [technique/docker/docker-compose.yml](technique/docker/docker-compose.yml) | Stack complète : API + PostgreSQL + MLflow + Prometheus + Grafana |
| [technique/docker/prometheus.yml](technique/docker/prometheus.yml) | Configuration Prometheus (scrape toutes les 10s) |
| [technique/.github/workflows/ci-cd.yml](technique/.github/workflows/ci-cd.yml) | Pipeline CI/CD : test → build ECR → staging → prod (blue-green) |

### Tests

| Fichier | Rôle |
|---|---|
| [technique/tests/unit/test_models.py](technique/tests/unit/test_models.py) | Tests unitaires : preprocessing, métriques, 4 modèles ML |
| [technique/tests/unit/test_api.py](technique/tests/unit/test_api.py) | Tests API : auth JWT, schemas Pydantic, endpoints FastAPI |
| [technique/tests/unit/test_drift.py](technique/tests/unit/test_drift.py) | Tests drift detection : KS Test, PSI, CUSUM |
| [technique/tests/load/locustfile.py](technique/tests/load/locustfile.py) | Tests de charge Locust : SLA 100 users, P95 < 500ms, erreur < 1% |

### Monitoring & Outils

| Fichier | Rôle |
|---|---|
| [technique/src/monitoring/drift.py](technique/src/monitoring/drift.py) | Détection dérive : KS Test, PSI, CUSUM — rapport et recommandations |
| [technique/Makefile](technique/Makefile) | Commandes Make : install, train, api, test, docker-up, load-test |
| [technique/docker/.env.example](technique/docker/.env.example) | Template variables d'environnement Docker |
| [technique/docker/init.sql](technique/docker/init.sql) | Schéma PostgreSQL : tables predictions et drift_metrics |

---

## RÉSUMÉ EXÉCUTIF DU PROJET

### Contexte

EDF souhaite moderniser sa prédiction de consommation électrique nationale en remplaçant ses modèles statistiques manuels (ARIMA) par une solution IA déployée dans le Cloud. Le projet implique 4 algorithmes ML (Réseau de neurones RBF, Forêt Aléatoire, Arbre de Décision, KNN), une API REST FastAPI conteneurisée sous Docker, et un pipeline CI/CD sur GitHub Actions.

### Résultats clés

| Indicateur | Résultat |
|---|---|
| **Meilleur modèle** | Random Forest — R² = 0,95 ; MAPE = 3,6 % |
| **Amélioration vs existant** | MAPE réduit de 8 % à 3,6 % (−55 %) |
| **Disponibilité SLA** | 99,5 % garantis |
| **Délai de production prédiction** | < 5 minutes (vs 2 jours) |
| **Budget** | 130 000 € sur 8 semaines |
| **Économies estimées** | 2 à 5 M€/an pour EDF |

### Choix méthodologiques clés

- **Scrum** avec sprints de 2 semaines — 4 sprints — 128 Story Points
- **Communication** : Microsoft Teams (principal) + Jira (backlog) + Confluence (documentation)
- **Cloud** : AWS EC2 + RDS PostgreSQL + S3 — région Paris (RGPD)
- **Modèle recommandé** : Forêt Aléatoire (meilleur R²/MAPE, le plus robuste en production)
- **Inclusion** : Charte d'équipe signée, 6 familles AGEFIPH adressées, outils accessibles WCAG 2.1

---

*MSPR TPRE932 & TPRE942 — Équipe EDF IA Predict — Avril 2026*
