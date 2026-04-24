# DOSSIER DE CADRAGE & CAHIER DES CHARGES DU PROJET EDF
## Projet EDF — Prédiction de la Consommation Électrique Journalière
### MSPR TPRE942 — Bloc de compétences 4 — Livrable 1

---

| Informations document | |
|---|---|
| **Version** | 1.0 |
| **Date** | Avril 2026 |
| **Auteurs** | Y. Morin (Chef de projet / Scrum Master), M. Dupont (PO / Business Analyst) |
| **Commanditaire** | EDF — Direction R&D |
| **Budget global** | 122 000 € |
| **Durée totale** | 8 semaines (4 sprints de 2 semaines) |

---

## TABLE DES MATIÈRES

1. Cadrage et planification du projet
2. Cahier des charges fonctionnel
3. Cahier des charges technique
4. Graphe PERT et chemin critique

---

## 1. CADRAGE ET PLANIFICATION DU PROJET

### 1.1 Objectifs du projet

#### Objectifs métier

| Objectif | Indicateur de succès | Valeur cible |
|---|---|---|
| Améliorer la précision des prévisions de consommation | MAPE | ≤ 4 % (vs 8 % actuellement) |
| Réduire les coûts liés aux achats d'énergie d'urgence | Économies annuelles | ≥ 2 M€/an |
| Accélérer la production des prévisions journalières | Délai de production | < 5 minutes (vs 2 jours) |
| Renforcer la position d'EDF dans la transition énergétique | Contribution R&D | Publication de résultats |

#### Objectifs techniques

| Objectif | Indicateur de succès | Valeur cible |
|---|---|---|
| Implémenter 4 algorithmes ML de prédiction | Nombre de modèles livrés | 4 (RBF, RF, DT, KNN) |
| Déployer la solution dans un conteneur Docker sur le Cloud | Service disponible | API accessible 24/7 |
| Mettre en place un pipeline CI/CD | Couverture des déploiements | 100 % des releases automatisées |
| Atteindre un niveau de disponibilité SLA | Uptime | ≥ 99,5 % |
| Assurer la traçabilité des modèles | Versioning MLflow | 100 % des expériences tracées |

### 1.2 Étapes de réalisation du système d'information

Le projet se déroule en **5 grandes étapes** correspondant au cycle de vie d'une solution IA :

| Étape | Description | Durée | Jalons |
|---|---|---|---|
| **E1 — Cadrage** | Collecte des besoins, analyse de l'existant, validation du périmètre | 1 semaine | J0 : Lancement officiel ; J7 : Validation du cadrage |
| **E2 — Conception** | Architecture technique, modélisation des données, conception des modèles IA | 1 semaine | J14 : Validation de l'architecture |
| **E3 — Développement & Tests** | Implémentation des 4 modèles, API FastAPI, Dockerisation, tests unitaires | 3 semaines | J35 : Recette technique |
| **E4 — Déploiement Pilote** | Déploiement sur AWS staging, tests de charge, validation métier | 2 semaines | J49 : Validation pilote |
| **E5 — Généralisation & Formation** | Déploiement production, documentation, formations utilisateurs | 1 semaine | J56 : Mise en production ; J56 : Livraison finale |

### 1.3 Découpage en tâches — WBS (Work Breakdown Structure)

```
PROJET EDF IA PREDICT
│
├── 1. CADRAGE
│   ├── 1.1 Réunion de lancement avec EDF (kick-off)
│   ├── 1.2 Collecte des besoins utilisateurs (interviews)
│   ├── 1.3 Analyse de l'existant (audit SI EDF)
│   ├── 1.4 Rédaction du cahier des charges fonctionnel
│   ├── 1.5 Rédaction du cahier des charges technique
│   └── 1.6 Validation du cadrage par le comité de pilotage
│
├── 2. CONCEPTION
│   ├── 2.1 Conception de l'architecture technique
│   ├── 2.2 Modélisation du schéma de base de données
│   ├── 2.3 Sélection et justification des algorithmes IA
│   ├── 2.4 Conception du pipeline de données (Airflow)
│   └── 2.5 Revue d'architecture (Architecture Review Board)
│
├── 3. DÉVELOPPEMENT & TESTS
│   ├── 3.1 Collecte et prétraitement des données RTE éco2mix
│   ├── 3.2 Feature engineering
│   ├── 3.3 Implémentation modèle RBF Neural Network
│   ├── 3.4 Implémentation modèle Random Forest
│   ├── 3.5 Implémentation modèle Arbre de Décision
│   ├── 3.6 Implémentation modèle KNN
│   ├── 3.7 Évaluation et comparaison des modèles (R², RMSE, MAPE)
│   ├── 3.8 Développement API FastAPI
│   ├── 3.9 Dockerisation de la solution
│   ├── 3.10 Mise en place pipeline CI/CD (GitHub Actions)
│   ├── 3.11 Configuration du monitoring (Prometheus + Grafana)
│   └── 3.12 Tests unitaires et d'intégration
│
├── 4. DÉPLOIEMENT PILOTE
│   ├── 4.1 Déploiement sur environnement AWS staging
│   ├── 4.2 Tests de charge (Locust)
│   ├── 4.3 Tests de résilience (Chaos Engineering)
│   ├── 4.4 Validation métier avec les ingénieurs EDF
│   └── 4.5 Corrections post-pilote
│
└── 5. GÉNÉRALISATION & FORMATION
    ├── 5.1 Déploiement en production (AWS EC2 prod)
    ├── 5.2 Rédaction de la documentation technique et du runbook
    ├── 5.3 Animation des formations utilisateurs
    ├── 5.4 Mise en place du support et de la hotline
    └── 5.5 Livraison et clôture du projet
```

### 1.4 Planification macro — Diagramme de Gantt

```
TÂCHES                              | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
─────────────────────────────────────────────────────────────────────────────
1.1 Kick-off                        | ██ |    |    |    |    |    |    |    |
1.2 Collecte besoins                | ██ |    |    |    |    |    |    |    |
1.3 Analyse existant                | ██ |    |    |    |    |    |    |    |
1.4 CDC Fonctionnel                 | ██ | ░░ |    |    |    |    |    |    |
1.5 CDC Technique                   | ██ | ░░ |    |    |    |    |    |    |
1.6 Validation cadrage              |    | ▲  |    |    |    |    |    |    |
2.1 Architecture technique          |    | ██ |    |    |    |    |    |    |
2.2 Schéma BDD                      |    | ██ |    |    |    |    |    |    |
2.3 Choix algorithmes               |    | ██ |    |    |    |    |    |    |
2.4 Pipeline données                |    | ██ |    |    |    |    |    |    |
2.5 Revue architecture              |    |    | ▲  |    |    |    |    |    |
3.1 Collecte + prétraitement data   |    |    | ██ |    |    |    |    |    |
3.2 Feature engineering             |    |    | ██ |    |    |    |    |    |
3.3 Modèle RBF                      |    |    | ██ | ░░ |    |    |    |    |
3.4 Modèle Random Forest            |    |    | ██ | ░░ |    |    |    |    |
3.5 Modèle Arbre de Décision        |    |    | ██ |    |    |    |    |    |
3.6 Modèle KNN                      |    |    |    | ██ |    |    |    |    |
3.7 Évaluation modèles              |    |    |    | ██ |    |    |    |    |
3.8 API FastAPI                     |    |    |    | ██ | ░░ |    |    |    |
3.9 Dockerisation                   |    |    |    |    | ██ |    |    |    |
3.10 Pipeline CI/CD                 |    |    |    |    | ██ |    |    |    |
3.11 Monitoring                     |    |    |    |    | ██ |    |    |    |
3.12 Tests                          |    |    |    |    | ██ | ░░ |    |    |
4.1 Déploiement staging             |    |    |    |    |    | ▲  |    |    |
4.2 Tests de charge                 |    |    |    |    |    | ██ |    |    |
4.3 Tests résilience                |    |    |    |    |    | ██ |    |    |
4.4 Validation métier               |    |    |    |    |    | ██ | ░░ |    |
4.5 Corrections                     |    |    |    |    |    |    | ██ |    |
5.1 Déploiement production          |    |    |    |    |    |    | ██ |    |
5.2 Documentation                   |    |    |    |    |    |    | ██ | ░░ |
5.3 Formations                      |    |    |    |    |    |    | ██ | ██ |
5.4 Support / Hotline               |    |    |    |    |    |    |    | ██ |
5.5 Livraison finale                |    |    |    |    |    |    |    | ▲  |

Légende : ██ = Tâche principale | ░░ = Tâche en chevauchement | ▲ = Jalon
S = Semaine
```

**Jalons clés (◆) :**
- **◆ J0 (S1)** — Lancement officiel du projet (kick-off)
- **◆ J14 (S2)** — Validation du cadrage et de l'architecture
- **◆ J35 (S5)** — Fin du développement et des tests techniques
- **◆ J42 (S6)** — Déploiement sur staging (environnement de test)
- **◆ J49 (S7)** — Validation du pilote par les utilisateurs EDF
- **◆ J56 (S8)** — Mise en production et livraison finale

### 1.5 Ressources humaines, techniques et financières

#### Ressources humaines

| Rôle | Profil | Charge (jours) | Coût journalier | Coût total |
|---|---|---|---|---|
| **Chef de projet / Scrum Master** | Y. Morin — Expert IA | 40 j | 700 €/j | 28 000 € |
| **Data Scientist / ML Engineer** | A. Bernard — Data Science | 40 j | 700 €/j | 28 000 € |
| **DevOps Engineer** | C. Nguyen — Cloud & DevOps | 35 j | 700 €/j | 24 500 € |
| **Business Analyst / PO** | M. Dupont — Business Analysis | 30 j | 700 €/j | 21 000 € |
| **Référent technique EDF** (client) | DSI EDF | 10 j | 0 (interne EDF) | 0 € |
| **TOTAL RESSOURCES HUMAINES** | | **155 j** | | **101 500 €** |

#### Ressources techniques

| Ressource | Description | Coût estimé |
|---|---|---|
| **AWS EC2** (3 instances prod + staging) | t3.xlarge × 2 prod, t3.medium × 1 staging | 1 800 €/8 semaines |
| **AWS RDS PostgreSQL** | Instance db.t3.medium, Multi-AZ | 600 €/8 semaines |
| **AWS S3** | Stockage modèles et données | 50 €/8 semaines |
| **GitHub Enterprise** | Versioning et CI/CD | 200 €/8 semaines |
| **MLflow** | Serveur tracking (hébergé sur EC2) | 0 € (open source) |
| **Prometheus + Grafana** | Monitoring (hébergé sur EC2) | 0 € (open source) |
| **Locust** | Tests de charge | 0 € (open source) |
| **TOTAL RESSOURCES TECHNIQUES** | | **2 650 €** |

#### Budget global synthétique

| Poste | Montant |
|---|---|
| Ressources humaines | 101 500 € |
| Infrastructure technique (8 semaines) | 2 650 € |
| Formations et accompagnement | 20 000 € |
| Contingence (5 %) | 6 207 € |
| **BUDGET TOTAL** | **130 357 €** *(arrondi à 130 000 €)* |

> **Note :** Ce budget est calculé pour une équipe de consultants externes. En intégrant des ressources EDF internes, le coût peut être réduit de 30 à 50 %.

---

## 2. CAHIER DES CHARGES FONCTIONNEL

### 2.1 Profil des acteurs (Personas)

| Persona | Rôle | Besoins fonctionnels | Niveau technique |
|---|---|---|---|
| **Ingénieur réseau EDF** | Dispatcher — pilote l'équilibre du réseau au quotidien | Prédictions J+1 disponibles dès 7h ; alertes en cas d'anomalie | Non-technique |
| **Data Analyst EDF** | Analyse les prédictions et gère les données | Accès aux données brutes et aux métriques de performance des modèles | Intermédiaire |
| **Acheteur d'énergie** | Achète l'électricité sur les marchés | Prédictions fiables pour planifier les achats anticipés | Non-technique |
| **Responsable R&D** | Pilote la direction scientifique | KPI de performance des modèles, rapports de synthèse | Expert |
| **Administrateur SI** | Gère l'infrastructure technique | Accès aux logs, monitoring, gestion des accès | Expert technique |

### 2.2 User Stories (Backlog Fonctionnel Priorisé)

#### ÉPIC 1 — Prédiction de consommation

| ID | User Story | Priorité | Critères d'acceptation |
|---|---|---|---|
| US01 | En tant qu'ingénieur réseau, je veux consulter la prédiction de consommation pour J+1 chaque matin avant 7h, afin de planifier le mix énergétique. | MUST | Prédiction disponible chaque jour avant 7h. Affichage en MW. Indicateur de confiance visible. |
| US02 | En tant qu'ingénieur réseau, je veux recevoir une alerte automatique si la prédiction s'écarte de plus de 10 % de la consommation habituelle, afin d'anticiper une situation exceptionnelle. | MUST | Alerte email + notification Teams envoyée dans les 15 min. Seuil d'alerte paramétrable. |
| US03 | En tant qu'acheteur, je veux consulter les prédictions sur 3 jours glissants, afin de planifier mes achats d'énergie sur les marchés. | SHOULD | Vue sur 3 jours. Export CSV disponible. |
| US04 | En tant que data analyst, je veux comparer les prédictions des 4 modèles IA sur un même graphique, afin d'identifier le plus performant dans le contexte actuel. | SHOULD | Vue comparative des 4 modèles. Métriques R², MAPE affichées. |
| US05 | En tant qu'ingénieur réseau, je veux soumettre un feedback sur une prédiction incorrecte, afin de contribuer à l'amélioration du modèle. | SHOULD | Formulaire accessible depuis le dashboard. Soumission en < 2 min. |

#### ÉPIC 2 — Monitoring et administration

| ID | User Story | Priorité | Critères d'acceptation |
|---|---|---|---|
| US06 | En tant qu'administrateur SI, je veux consulter l'état de santé de l'API en temps réel, afin de détecter rapidement une panne. | MUST | Dashboard Grafana accessible. Indicateur vert/orange/rouge. Alerte si indisponibilité > 1 min. |
| US07 | En tant que data analyst, je veux être notifié si les performances du modèle se dégradent (MAPE > 5 %), afin de déclencher un ré-entraînement. | MUST | Alerte email automatique. Rapport hebdomadaire de performance. |
| US08 | En tant qu'administrateur, je veux gérer les droits d'accès des utilisateurs (RBAC), afin de sécuriser l'accès à la solution. | MUST | Interface d'administration. Rôles : Admin, User, Viewer. Authentification JWT. |

#### ÉPIC 3 — Reporting

| ID | User Story | Priorité | Critères d'acceptation |
|---|---|---|---|
| US09 | En tant que responsable R&D, je veux recevoir un rapport mensuel automatisé sur les performances des modèles, afin de suivre l'évolution de la précision. | SHOULD | Rapport PDF/Excel généré automatiquement le 1er de chaque mois. |
| US10 | En tant qu'acheteur d'énergie, je veux exporter les prédictions au format CSV, afin de les intégrer dans mes outils de planification. | COULD | Export CSV en 1 clic depuis le dashboard. |

### 2.3 Règles de gestion

| ID | Règle | Description |
|---|---|---|
| RG01 | Disponibilité | La prédiction J+1 doit être disponible chaque jour avant 7h00 (heure de Paris), 7j/7 |
| RG02 | Fraîcheur des données | Les données d'entrée ne peuvent pas avoir plus de 48h d'ancienneté |
| RG03 | Seuil d'alerte | Une alerte est déclenchée automatiquement si le MAPE dépasse 5 % pendant 3 jours consécutifs |
| RG04 | Modèle principal | La Forêt Aléatoire est le modèle de référence pour les décisions opérationnelles |
| RG05 | Validation humaine | Toute décision de délestage ou d'achat d'urgence basée sur l'IA nécessite une validation humaine |
| RG06 | Droits d'accès | L'accès à l'API est restreint aux utilisateurs authentifiés (JWT) — pas d'accès anonyme |
| RG07 | Rétention des données | Les prédictions et les données d'entrée sont conservées 5 ans |
| RG08 | RGPD | Aucune donnée personnelle identifiable n'est traitée ou stockée |

### 2.4 Indicateurs de performance (KPI fonctionnels)

| KPI | Description | Valeur cible | Fréquence de mesure |
|---|---|---|---|
| **Taux de disponibilité du service** | % de temps où l'API est accessible | ≥ 99,5 % | Continue |
| **MAPE moyen mensuel** | Erreur moyenne de prédiction | ≤ 4 % | Mensuelle |
| **Taux d'adoption** | % d'utilisateurs actifs vs licenciés | ≥ 80 % à M+3 | Mensuelle |
| **Délai de production des prédictions** | Temps entre déclenchement et résultat disponible | < 5 minutes | Quotidienne |
| **Score de satisfaction NPS** | Satisfaction utilisateurs | ≥ 7/10 | Trimestrielle |

### 2.5 Dates clés des livrables fonctionnels

| Livrable | Date de livraison | Responsable |
|---|---|---|
| Validation du cahier des charges fonctionnel | J+14 | PO + Chef de projet |
| Démonstration des 4 modèles IA implémentés | J+35 | Data Scientist |
| Dashboard de prédiction opérationnel (staging) | J+42 | DevOps + Data Scientist |
| Recette utilisateurs (UAT) | J+49 | PO + Ingénieurs EDF |
| Mise en production | J+56 | DevOps + Chef de projet |
| Bilan à 1 mois post-production | J+86 | Chef de projet |

---

## 3. CAHIER DES CHARGES TECHNIQUE

### 3.1 Contraintes d'architecture

| Contrainte | Description | Justification |
|---|---|---|
| **Conteneurisation obligatoire** | Toute la solution doit être packagée en Docker | Reproductibilité des déploiements, portabilité |
| **Cloud provider : AWS** | Hébergement sur AWS (région eu-west-3 Paris) | Conformité RGPD (données sur territoire européen), partenariat EDF-AWS |
| **API RESTful** | Interface de communication via API REST (JSON) | Interopérabilité avec le SI EDF existant |
| **Haute disponibilité** | Architecture redondante (minimum 2 instances) | SLA 99,5 % |
| **Open source** | Les frameworks et librairies ML doivent être open source | Maîtrise des coûts de licence |
| **Python exclusivement** | Langage de développement unique | Cohérence de la stack, compétences de l'équipe |

### 3.2 Données

| Aspect | Spécification |
|---|---|
| **Source principale** | RTE éco2mix (API publique et historiques téléchargeables) |
| **Données météo** | API Météo France (température nationale moyenne journalière) |
| **Volume** | 5 ans de données horaires ≈ 43 800 enregistrements |
| **Format d'ingestion** | JSON (API RTE) → Pandas DataFrame → PostgreSQL |
| **Fréquence de mise à jour** | Quotidienne (pipeline Airflow à 02h00) |
| **Qualité des données** | Taux de valeurs manquantes toléré : < 0,5 % ; Outliers traités par médiane glissante 7j |
| **Stockage** | PostgreSQL (données structurées) + AWS S3 (datasets bruts, modèles sérialisés) |

### 3.3 Contraintes de performance

| Critère | Spécification |
|---|---|
| **Temps de réponse API (p50)** | < 500 ms |
| **Temps de réponse API (p95)** | < 2 000 ms |
| **Débit maximum** | 200 requêtes/seconde (dimensionnement AWS) |
| **Temps de ré-entraînement** | < 30 minutes pour 5 ans de données |
| **Temps de déploiement d'une nouvelle version** | < 10 minutes (pipeline CI/CD) |
| **Capacité de stockage** | 100 Go SSD minimum en production |
| **Uptime** | ≥ 99,5 % (maintenance planifiée exclue) |

### 3.4 Sécurité

| Aspect | Spécification |
|---|---|
| **Transport** | HTTPS obligatoire (TLS 1.3) — redirection automatique HTTP → HTTPS |
| **Authentification** | JWT (JSON Web Tokens) — expiration 24h |
| **Autorisation** | RBAC (Role-Based Access Control) — 3 rôles : Admin, User, Viewer |
| **Gestion des secrets** | AWS Secrets Manager (prod) / .env fichier (dev, hors Git) |
| **Sécurité réseau** | AWS Security Groups — ports ouverts : 443 (HTTPS) uniquement depuis internet |
| **Logs de sécurité** | Audit trail de tous les accès authentifiés — rétention 12 mois |
| **Analyse de vulnérabilités** | Scan automatique des images Docker via Trivy (intégré au pipeline CI/CD) |
| **RGPD** | Aucune donnée personnelle — données agrégées nationales uniquement |

### 3.5 Intégrations avec les systèmes existants

| Système EDF | Type d'intégration | Protocole | Responsable |
|---|---|---|---|
| **SI EDF (SAP)** | Lecture des calendriers (jours fériés, événements planifiés) | API REST interne EDF | DSI EDF |
| **Portail intranet EDF** | Intégration du dashboard Streamlit en iframe | HTTPS | DevOps |
| **Système d'alertes EDF** | Envoi des alertes de prédiction via webhook | HTTPS POST | DevOps |
| **Microsoft Teams** | Notifications automatiques (canal dédié) | Teams Connector | DevOps |
| **API RTE éco2mix** | Ingestion quotidienne des données de consommation | API REST publique | Data Scientist |

---

## 4. GRAPHE PERT ET CHEMIN CRITIQUE

### 4.1 Identification des tâches et dépendances

| ID Tâche | Nom | Durée (jours) | Prédécesseurs |
|---|---|---|---|
| A | Kick-off et collecte des besoins | 3 | — |
| B | Rédaction CDC fonctionnel & technique | 4 | A |
| C | Validation du cadrage (jalon) | 1 | B |
| D | Conception architecture technique | 3 | C |
| E | Modélisation schéma BDD | 2 | C |
| F | Conception pipeline de données (Airflow) | 2 | D |
| G | Collecte et prétraitement des données | 3 | F, E |
| H | Feature engineering | 2 | G |
| I | Implémentation modèle RBF | 4 | H |
| J | Implémentation modèle Random Forest | 3 | H |
| K | Implémentation modèle Arbre de Décision | 2 | H |
| L | Implémentation modèle KNN | 2 | H |
| M | Évaluation et comparaison des modèles | 2 | I, J, K, L |
| N | Développement API FastAPI | 4 | M |
| O | Dockerisation de la solution | 2 | N |
| P | Pipeline CI/CD (GitHub Actions) | 2 | O |
| Q | Configuration monitoring (Prometheus+Grafana) | 2 | O |
| R | Tests unitaires et d'intégration | 3 | P, Q |
| S | Déploiement staging AWS | 1 | R |
| T | Tests de charge (Locust) | 2 | S |
| U | Tests de résilience (Chaos) | 2 | S |
| V | Validation métier avec EDF | 3 | T, U |
| W | Corrections post-pilote | 2 | V |
| X | Déploiement production AWS | 1 | W |
| Y | Documentation et formations | 4 | X |
| Z | Livraison finale et clôture | 1 | Y |

### 4.2 Graphe PERT — Représentation textuelle

```
Début
  │
  ▼
[A] 3j ──► [B] 4j ──► [C] 1j ──► [D] 3j ──► [F] 2j ──► [G] 3j ──► [H] 2j
                                    │                              │
                                    └──► [E] 2j ─────────────────►┘

[H] 2j ──► [I] 4j ─────────────────────────────────────────► [M] 2j
     │──► [J] 3j ──────────────────────────────────────────►│
     │──► [K] 2j ──────────────────────────────────────────►│
     └──► [L] 2j ──────────────────────────────────────────►┘

[M] 2j ──► [N] 4j ──► [O] 2j ──► [P] 2j ──► [R] 3j ──► [S] 1j
                             │                              │
                             └──► [Q] 2j ─────────────────►┘

[S] 1j ──► [T] 2j ──► [V] 3j ──► [W] 2j ──► [X] 1j ──► [Y] 4j ──► [Z] 1j
     │──► [U] 2j ──►│
```

### 4.3 Calcul du chemin critique

Pour chaque tâche, calcul des **dates au plus tôt (EST)** et **dates au plus tard (LST)** :

| Tâche | EST | EFT | LST | LFT | Marge | Critique ? |
|---|---|---|---|---|---|---|
| A | 0 | 3 | 0 | 3 | 0 | **OUI** |
| B | 3 | 7 | 3 | 7 | 0 | **OUI** |
| C | 7 | 8 | 7 | 8 | 0 | **OUI** |
| D | 8 | 11 | 8 | 11 | 0 | **OUI** |
| E | 8 | 10 | 9 | 11 | 1 | Non |
| F | 11 | 13 | 11 | 13 | 0 | **OUI** |
| G | 13 | 16 | 13 | 16 | 0 | **OUI** |
| H | 16 | 18 | 16 | 18 | 0 | **OUI** |
| I | 18 | 22 | 18 | 22 | 0 | **OUI** |
| J | 18 | 21 | 19 | 22 | 1 | Non |
| K | 18 | 20 | 20 | 22 | 2 | Non |
| L | 18 | 20 | 20 | 22 | 2 | Non |
| M | 22 | 24 | 22 | 24 | 0 | **OUI** |
| N | 24 | 28 | 24 | 28 | 0 | **OUI** |
| O | 28 | 30 | 28 | 30 | 0 | **OUI** |
| P | 30 | 32 | 30 | 32 | 0 | **OUI** |
| Q | 30 | 32 | 30 | 32 | 0 | **OUI** |
| R | 32 | 35 | 32 | 35 | 0 | **OUI** |
| S | 35 | 36 | 35 | 36 | 0 | **OUI** |
| T | 36 | 38 | 36 | 38 | 0 | **OUI** |
| U | 36 | 38 | 36 | 38 | 0 | **OUI** |
| V | 38 | 41 | 38 | 41 | 0 | **OUI** |
| W | 41 | 43 | 41 | 43 | 0 | **OUI** |
| X | 43 | 44 | 43 | 44 | 0 | **OUI** |
| Y | 44 | 48 | 44 | 48 | 0 | **OUI** |
| Z | 48 | 49 | 48 | 49 | 0 | **OUI** |

### 4.4 Chemin critique identifié

**Durée totale du projet : 49 jours ouvrés (≈ 8 semaines)**

```
CHEMIN CRITIQUE :
A → B → C → D → F → G → H → I → M → N → O → P → R → S → T → V → W → X → Y → Z
```

**Tâches à risque (marge = 0) :** Toutes les tâches du chemin critique. Un retard sur l'une d'elles se répercute directement sur la date de livraison finale.

**Tâches avec marge :**
- Tâche E (Schéma BDD) : 1 jour de marge — peut démarrer un jour plus tard sans impact
- Tâches J, K, L (Modèles RF, DT, KNN) : 1 à 2 jours de marge — le modèle RBF (le plus long) dicte le rythme

**Actions préventives sur le chemin critique :**
- Attribution de deux développeurs sur la tâche I (Modèle RBF) pour réduire la durée à 3j
- Tests automatisés dès le développement (TDD) pour réduire le temps de recette (tâche R)
- Déploiement staging préparé en avance (infrastructure AWS provisionnée dès S4)

---

*Document rédigé par l'équipe projet MSPR EDF — Avril 2026*
*Référence : MSPR-TPRE942-B4-L1-v1.0*
