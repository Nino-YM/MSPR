# DOSSIER DE PILOTAGE AGILE & SUIVI DU PROJET
## Projet EDF — Prédiction de la Consommation Électrique Journalière
### MSPR TPRE942 — Bloc de compétences 4 — Livrable 2

---

| Informations document | |
|---|---|
| **Version** | 1.0 |
| **Date** | Avril 2026 |
| **Auteurs** | Y. Morin (Scrum Master), M. Dupont (Product Owner) |
| **Méthode agile** | Scrum (sprints de 2 semaines) |

---

## TABLE DES MATIÈRES

1. Organisation agile du projet
2. Backlog produit
3. Tableaux de bord de suivi du projet
4. Pilotage des prestataires et du SI existant

---

## 1. ORGANISATION AGILE DU PROJET

### 1.1 Méthode choisie : SCRUM

#### Justification du choix de Scrum

La méthode **Scrum** a été retenue pour ce projet pour les raisons suivantes :

| Critère | Justification |
|---|---|
| **Complexité et incertitude** | Le projet IA comporte des incertitudes sur les performances des modèles — Scrum permet d'itérer rapidement et d'ajuster la priorité du backlog en fonction des résultats |
| **Livraisons fréquentes de valeur** | EDF souhaite valider les résultats intermédiaires (modèles, API) et non attendre la livraison finale |
| **Équipe petite et co-localisée** | 4 membres — taille idéale pour Scrum (3 à 9 personnes selon le Scrum Guide) |
| **Engagement client fort** | Le référent EDF est impliqué comme stakeholder et peut participer aux Sprint Reviews |
| **Amélioration continue** | Les rétrospectives permettent d'ajuster les pratiques d'une équipe qui travaille ensemble pour la première fois |

**Scrum vs autres méthodes :**
- **Kanban** écarté : moins adapté pour un projet avec une échéance fixe et des livrables planifiés
- **SAFe** écarté : trop complexe pour une équipe de 4 personnes
- **FDD (Feature-Driven Development)** écarté : moins de support communautaire et d'outillage

### 1.2 Rôles Scrum

| Rôle | Personne | Responsabilités |
|---|---|---|
| **Product Owner (PO)** | M. Dupont | Définir et prioriser le Product Backlog ; représenter les intérêts d'EDF ; valider les livraisons à chaque Sprint Review ; gérer la roadmap fonctionnelle |
| **Scrum Master** | Y. Morin | Faciliter les cérémonies Scrum ; lever les obstacles (impediments) ; protéger l'équipe de toute interruption externe ; accompagner l'équipe dans l'adoption des pratiques agiles |
| **Équipe de développement** | A. Bernard (Data Science) + C. Nguyen (DevOps) + Y. Morin (Développement) | Concevoir, développer, tester et livrer les fonctionnalités à chaque sprint ; auto-organisation |
| **Stakeholders (parties prenantes)** | Référent EDF (DSI), Ingénieurs réseau EDF | Participer aux Sprint Reviews ; fournir les feedbacks ; valider les résultats métier |

### 1.3 Outil de communication — Microsoft Teams

L'outil de communication principal de l'équipe est **Microsoft Teams**, choisi car :
- Déjà déployé dans l'infrastructure EDF (licence existante)
- Intégration native avec GitHub (notifications des commits et pull requests)
- Adapté aux équipes distribuées (France + sites EDF à l'international)
- Respect de la politique de sécurité EDF (données hébergées sur serveurs Microsoft Europe)

**Organisation des canaux Teams :**

| Canal | Objectif | Participants |
|---|---|---|
| `#general` | Annonces importantes, informations générales | Toute l'équipe + Stakeholders |
| `#daily-standup` | Résumés écrits du daily meeting | Équipe de développement |
| `#dev-ml` | Discussions techniques ML et data | Data Scientist + DevOps |
| `#devops-infra` | Infrastructure, CI/CD, Docker | DevOps + Chef de projet |
| `#sprint-review` | Comptes-rendus des Sprint Reviews | Toute l'équipe + Stakeholders EDF |
| `#alertes-monitoring` | Notifications automatiques (Grafana, GitHub Actions) | DevOps + Chef de projet |
| `#random` | Discussions informelles, team building | Toute l'équipe |

**Processus de check-in / check-out quotidien :**

Chaque matin à 9h30, chaque membre poste dans `#daily-standup` :
```
🟢 CHECK-IN [NOM] — [DATE]
✅ Hier : [Ce que j'ai fait]
🎯 Aujourd'hui : [Ce que je vais faire]
🚧 Blocages : [Aucun / Description du blocage]
```

En fin de journée (18h) :
```
🔵 CHECK-OUT [NOM]
📊 Avancement : [% de la tâche en cours]
📝 Note : [Élément important à noter]
```

### 1.4 Outil de centralisation des tâches — Jira

L'équipe utilise **Jira Software** pour la gestion du backlog et le suivi des sprints.

**Configuration Jira :**
- **Projet :** EDF-PREDICT
- **Board type :** Scrum Board
- **Sprint length :** 2 semaines
- **Statuts des tickets :** To Do → In Progress → Code Review → Testing → Done

**Workflow Jira :**
```
[PRODUCT BACKLOG]
    │
    ▼ (Sprint Planning)
[SPRINT BACKLOG]
    │
    ▼
[TO DO] ──► [IN PROGRESS] ──► [CODE REVIEW] ──► [TESTING] ──► [DONE]
              (Développeur)      (Pair review)    (QA/Tests)   (DoD ✓)
```

**Intégrations Jira :**
- GitHub : lien automatique commit ↔ ticket (ex : `git commit -m "EDF-42: Implement Random Forest model"`)
- Microsoft Teams : notifications automatiques lors des changements de statut
- Confluence : documentation liée aux tickets

### 1.5 Cérémonies Scrum

| Cérémonie | Fréquence | Durée | Participants | Objectif |
|---|---|---|---|---|
| **Sprint Planning** | Début de chaque sprint | 2 h max | Toute l'équipe + PO | Sélectionner et décomposer les User Stories du sprint ; définir le Sprint Goal |
| **Daily Scrum** | Chaque jour ouvré (9h30) | 15 min strictes | Équipe de développement | Synchroniser les activités ; identifier les blocages |
| **Sprint Review** | Fin de chaque sprint | 1 h | Toute l'équipe + Stakeholders EDF | Démontrer les fonctionnalités livrées ; recueillir les feedbacks |
| **Sprint Retrospective** | Fin de chaque sprint | 1 h | Toute l'équipe (sans stakeholders) | Amélioration continue des pratiques d'équipe |
| **Backlog Refinement** | 1 fois par semaine (milieu de sprint) | 30 min | PO + Scrum Master + équipe | Affiner, estimer et prioriser les User Stories à venir |

### 1.6 Définition of Ready (DoR) et Définition of Done (DoD)

#### Definition of Ready (DoR) — Conditions pour entrer en sprint
- [ ] La User Story est rédigée selon le format standard (En tant que... je veux... afin de...)
- [ ] Les critères d'acceptation sont définis et validés par le PO
- [ ] La complexité est estimée en Story Points (Planning Poker)
- [ ] Les dépendances techniques sont identifiées
- [ ] La User Story peut être complétée en un sprint (≤ 13 Story Points)

#### Definition of Done (DoD) — Conditions pour valider une User Story
- [ ] Le code est développé et fonctionne sur l'environnement de développement
- [ ] Les tests unitaires sont écrits et passent (couverture ≥ 80 %)
- [ ] La Pull Request est approuvée par au moins 1 pair (code review)
- [ ] Les tests d'intégration passent sur l'environnement de staging
- [ ] La documentation est mise à jour (si applicable)
- [ ] La User Story est démontrée et validée par le PO lors de la Sprint Review
- [ ] Le ticket Jira est marqué "Done"

### 1.7 Déroulement des 4 sprints

| Sprint | Semaines | Sprint Goal | User Stories incluses |
|---|---|---|---|
| **Sprint 1** | S1-S2 | "Cadrer le projet et concevoir l'architecture" | US: Cadrage, CDC, Architecture, Schéma BDD, Pipeline données |
| **Sprint 2** | S3-S4 | "Implémenter et comparer les 4 modèles IA" | US: Prétraitement, Feature engineering, 4 modèles, Évaluation |
| **Sprint 3** | S5-S6 | "Déployer la solution en conteneur et la monitorer" | US: API, Docker, CI/CD, Monitoring, Tests de charge |
| **Sprint 4** | S7-S8 | "Valider avec EDF et livrer la solution complète" | US: Validation métier, Corrections, Documentation, Formations |

---

## 2. BACKLOG PRODUIT

### 2.1 Épics et User Stories priorisées (MoSCoW)

| ID | Épic | User Story | Story Points | Priorité MoSCoW | Sprint |
|---|---|---|---|---|---|
| US01 | Prédiction | Prédiction J+1 disponible avant 7h | 8 | MUST | S3 |
| US02 | Prédiction | Alerte si écart > 10 % | 5 | MUST | S3 |
| US03 | Prédiction | Prédictions sur 3 jours glissants | 3 | SHOULD | S3 |
| US04 | Prédiction | Comparaison des 4 modèles sur graphique | 5 | SHOULD | S3 |
| US05 | Prédiction | Formulaire de feedback | 3 | SHOULD | S4 |
| US06 | Monitoring | Dashboard santé API en temps réel | 5 | MUST | S3 |
| US07 | Monitoring | Alerte MAPE > 5 % | 3 | MUST | S3 |
| US08 | Admin | Gestion des droits d'accès (RBAC) | 5 | MUST | S3 |
| US09 | Reporting | Rapport mensuel automatisé | 3 | SHOULD | S4 |
| US10 | Reporting | Export CSV des prédictions | 2 | COULD | S4 |
| US11 | Infrastructure | Déploiement Docker sur AWS | 8 | MUST | S3 |
| US12 | Infrastructure | Pipeline CI/CD GitHub Actions | 5 | MUST | S3 |
| US13 | Data | Ingestion quotidienne RTE éco2mix | 5 | MUST | S2 |
| US14 | Data | Prétraitement et feature engineering | 8 | MUST | S2 |
| US15 | ML | Implémentation Random Forest | 8 | MUST | S2 |
| US16 | ML | Implémentation RBF Neural Network | 13 | MUST | S2 |
| US17 | ML | Implémentation Arbre de Décision | 5 | MUST | S2 |
| US18 | ML | Implémentation KNN | 5 | MUST | S2 |
| US19 | ML | Évaluation comparative (R², RMSE, MAPE) | 5 | MUST | S2 |
| US20 | Docs | Documentation technique et runbook | 5 | MUST | S4 |
| US21 | Formation | Formations utilisateurs EDF | 8 | MUST | S4 |
| US22 | Formation | Guide d'utilisation IA | 3 | MUST | S4 |

**Total : 128 Story Points** répartis sur 4 sprints (moyenne : 32 SP / sprint — cohérent avec la vélocité d'une équipe de 4 personnes)

### 2.2 Vélocité par sprint (prévisionnel vs réel)

| Sprint | Vélocité Prévisionnelle | Vélocité Réelle | Écart | Explication |
|---|---|---|---|---|
| Sprint 1 | 28 SP | 26 SP | -2 SP | Kick-off plus long que prévu — stakeholders EDF nombreux |
| Sprint 2 | 44 SP | 47 SP | +3 SP | RBF plus rapide que prévu grâce à l'utilisation de Keras |
| Sprint 3 | 29 SP | 27 SP | -2 SP | Bug d'authentification JWT résolu mais temps perdu |
| Sprint 4 | 27 SP | 28 SP | +1 SP | Finalisation dans les temps |
| **TOTAL** | **128 SP** | **128 SP** | **0** | **Projet livré dans les délais** |

---

## 3. TABLEAUX DE BORD DE SUIVI DU PROJET

### 3.1 KPI projet — Vue synthétique

| Axe | KPI | Description | Valeur cible | Mesure |
|---|---|---|---|---|
| **Avancement** | Burndown Chart (Story Points restants) | Points restants / Points total | 0 SP à J+56 | Jira — quotidien |
| **Avancement** | Taux d'achèvement des tâches par sprint | % US Done / US planifiées | ≥ 90 % par sprint | Jira — fin de sprint |
| **Charges** | Taux d'utilisation des ressources | Heures consommées / Heures budgétées | 90 à 110 % | Jira time tracking — hebdo |
| **Qualité** | Taux de couverture de code | % de code couvert par les tests | ≥ 80 % | GitHub Actions — CI |
| **Qualité** | Nombre d'anomalies ouvertes | Tickets de type "Bug" en statut "Open" | ≤ 3 bugs mineurs actifs | Jira — quotidien |
| **Qualité** | Taux de bugs détectés en production | Bugs prod / Bugs total | < 10 % | Post-production |
| **Performance ML** | MAPE du meilleur modèle | Erreur de prédiction | ≤ 4 % | MLflow — après S2 |
| **Vélocité** | Vélocité sprint | Story Points livrés / Sprint | ≥ 28 SP / sprint | Jira — fin de sprint |

### 3.2 Burndown Chart — Sprint 2 (exemple détaillé)

```
Story Points
restants
│
44 ┤ ●
   │  ╲  ─ ─ ─ Ligne idéale (objectif)
40 ┤   ╲
   │    ●
36 ┤     ╲
   │      ╲
32 ┤       ● ●  ← Ligne réelle (légèrement au-dessus = légèrement en retard j5-j6)
   │           ╲
28 ┤            ●
   │             ╲
24 ┤              ╲
   │               ●
20 ┤                ╲
   │                 ╲
16 ┤                  ●
   │                   ╲
12 ┤                    ╲
   │                     ●
 8 ┤                      ╲
   │                       ╲
 4 ┤                        ●
   │                         ╲
 0 ┤──────────────────────────●
   └─┬──┬──┬──┬──┬──┬──┬──┬──┬──►
    J1  J2  J3  J4  J5  J6  J7  J8  J9  J10
                         (Jours du sprint)

Sprint 2 : 10 jours ouvrés / 44 Story Points
Résultat réel : 47 SP livrés (3 SP supplémentaires issus du backlog)
```

### 3.3 Vue Sponsor — Tableau de bord de pilotage

**Destiné au responsable EDF / Direction R&D — Mise à jour hebdomadaire**

```
╔══════════════════════════════════════════════════════════════════╗
║        TABLEAU DE BORD EDF IA PREDICT — SEMAINE 6              ║
╠══════════════════════════════════════════════════════════════════╣
║  AVANCEMENT GLOBAL                                              ║
║  ████████████████████░░░░░░ 75 %   (Sprint 3 / 4)             ║
╠══════════════════════════════════════════════════════════════════╣
║  DÉLAIS           ✅ DANS LES TEMPS    Date liv. : 18 mai 2026  ║
║  BUDGET           ✅ DANS LES CLOUS    Consommé : 89 500 €      ║
║                                        Restant : 32 500 €       ║
║  QUALITÉ ML       ✅ OBJECTIF ATTEINT  MAPE = 3,6 % (cible ≤4%)║
║  RISQUES          🟡 1 RISQUE MODÉRÉ   Voir détail ci-dessous   ║
╠══════════════════════════════════════════════════════════════════╣
║  FAITS MARQUANTS SEMAINE 6                                      ║
║  ✅ Déploiement AWS staging réussi                              ║
║  ✅ Tests de charge OK (200 utilisateurs simultanés)            ║
║  🟡 Bug JWT corrigé — 1 jour de retard absorbé par la marge    ║
║  📅 Sprint Review S3 : vendredi 9 mai — invitation envoyée      ║
╠══════════════════════════════════════════════════════════════════╣
║  PROCHAINES ÉTAPES                                              ║
║  S7 : Validation métier avec les ingénieurs EDF                 ║
║  S8 : Déploiement production + formations                       ║
╚══════════════════════════════════════════════════════════════════╝
```

### 3.4 Vue Chef de Projet — Suivi détaillé

| Semaine | Sprint | US Planifiées | US Done | % Completion | Bugs Ouverts | Budget Consommé |
|---|---|---|---|---|---|---|
| S1 | Sprint 1 | 8 | 7 | 87 % | 0 | 14 200 € |
| S2 | Sprint 1 | 8 | 8 | 100 % | 1 | 28 400 € |
| S3 | Sprint 2 | 10 | 9 | 90 % | 2 | 42 600 € |
| S4 | Sprint 2 | 10 | 12 | 120 % | 0 | 56 800 € |
| S5 | Sprint 3 | 8 | 7 | 87 % | 1 | 68 500 € |
| S6 | Sprint 3 | 8 | 7 | 87 % | 2 | 80 200 € |
| S7 | Sprint 4 | 7 | — | En cours | — | ~95 000 € |
| S8 | Sprint 4 | 7 | — | En cours | — | ~122 000 € |

### 3.5 Comment les indicateurs sont utilisés pour corriger les écarts

#### Exemple de décision prise suite aux indicateurs — Semaine 5

**Situation détectée :** À la fin de la semaine 5, le Burndown Chart montre un retard de 5 Story Points par rapport à la ligne idéale. Le bug JWT (authentification API) est ouvert depuis 2 jours.

**Analyse en Daily Scrum :**
- Cause identifiée : La librairie JWT utilisée (python-jose) a un comportement incompatible avec la version Python 3.11.
- Impact estimé : 1 jour de retard sur la livraison de l'US08 (RBAC).

**Décision prise :**
1. Basculement vers la librairie `python-jwt` (solution alternative identifiée en 30 min)
2. Le DevOps et le Data Scientist switchent pour 1 jour sur ce bug — en binôme pour aller plus vite
3. Le PO accepte de reporter l'US10 (Export CSV) au Sprint 4 pour absorber le retard
4. Le Scrum Master met à jour le Burndown Chart et informe les stakeholders EDF

**Résultat :** Bug corrigé en 6 heures. Retard rattrapé dès le lendemain. Aucun impact sur la livraison finale.

---

## 4. PILOTAGE DES PRESTATAIRES ET DU SI EXISTANT

### 4.1 Cartographie des prestataires et systèmes existants

| Entité | Type | Rôle dans le projet | Contact référent |
|---|---|---|---|
| **AWS** | Hébergeur Cloud | Infrastructure de production et staging (EC2, RDS, S3, ECR) | Account Manager AWS France |
| **GitHub** | Gestionnaire de code | Versioning, CI/CD (GitHub Actions), code review | Support GitHub Enterprise |
| **Microsoft Teams** | Communication | Canal de communication principal | DSI EDF (licence existante) |
| **Confluence / Jira** | Gestion de projet | Backlog, documentation, suivi | Atlassian Support |
| **RTE** | Fournisseur de données | API éco2mix — données de consommation | Portail développeur RTE |
| **Météo France** | Fournisseur de données | API météo — données de température | Portail Météo France Entreprise |
| **DSI EDF** | SI existant | Intégration calendrier EDF, gestion des accès, portail intranet | Référent technique EDF DSI |

### 4.2 Tableau de bord prestataires — Suivi SLA

| Prestataire | Nature prestation | Type SLA | Disponibilité garantie | Délai de résolution incident | Durée contrat | Coût mensuel |
|---|---|---|---|---|---|---|
| **AWS** | Infrastructure Cloud (EC2, RDS, S3) | SLA Gold | 99,99 % | P1 < 1h ; P2 < 4h | 12 mois | 350 € |
| **GitHub Enterprise** | SCM + CI/CD | SLA Standard | 99,9 % | P1 < 4h ; P2 < 24h | 12 mois | 25 € |
| **Jira / Confluence** (Atlassian Cloud) | Gestion de projet | SLA Standard | 99,9 % | P1 < 4h | 12 mois | 60 € |
| **RTE éco2mix API** | Données de consommation | Best effort (public) | Non garanti | N/A | Sans contrat | 0 € |
| **Météo France API** | Données météo | SLA Professionnel | 99,5 % | P1 < 8h | 12 mois | 150 € |

### 4.3 Indicateurs de performance par prestataire

| Prestataire | KPI principal | Valeur cible | Valeur actuelle | Statut |
|---|---|---|---|---|
| **AWS** | Uptime des instances EC2 | ≥ 99,9 % | 99,97 % | ✅ OK |
| **AWS** | Latence RDS (p95) | < 50 ms | 32 ms | ✅ OK |
| **GitHub** | Disponibilité Actions CI/CD | ≥ 99,5 % | 99,8 % | ✅ OK |
| **RTE éco2mix** | Disponibilité de l'API d'ingestion | ≥ 95 % (best effort) | 98,2 % | ✅ OK |
| **Météo France** | Disponibilité de l'API météo | ≥ 99,5 % | 99,6 % | ✅ OK |
| **Jira / Confluence** | Disponibilité de la plateforme | ≥ 99,5 % | 99,9 % | ✅ OK |

### 4.4 Pénalités contractuelles (SLA)

| Prestataire | Niveau SLA non respecté | Pénalité |
|---|---|---|
| **AWS** | Uptime < 99,9 % mensuel | Crédit de service de 10 % de la facture mensuelle |
| **AWS** | Uptime < 99,0 % mensuel | Crédit de service de 30 % |
| **Météo France** | Uptime < 99,5 % mensuel | Réduction de 15 % sur la facture mensuelle |
| **GitHub** | Uptime < 99,9 % mensuel | Crédit de service de 25 % |

### 4.5 Fréquence de suivi des prestataires

| Prestataire | Suivi quotidien | Suivi hebdomadaire | Suivi mensuel | Comité trimestriel |
|---|---|---|---|---|
| **AWS** | Dashboard CloudWatch + Grafana | Rapport automatisé d'utilisation | Facture + rapport SLA | Revue de contrat si évolution |
| **RTE éco2mix** | Vérification de l'ingestion quotidienne (Airflow) | Analyse des données manquantes | Rapport de qualité des données | Non applicable |
| **Météo France** | Vérification de l'ingestion quotidienne | — | Rapport SLA | — |
| **GitHub / Jira** | Tableau de bord Jira | Sprint Backlog + vélocité | Rapport sprint + qualité CI/CD | Évolution licences |

### 4.6 Matrice RACI — Pilotage prestataires

| Activité | Chef de projet | DevOps | Data Scientist | DSI EDF |
|---|---|---|---|---|
| Suivi quotidien AWS (CloudWatch) | I | **R/A** | I | I |
| Suivi quotidien ingestion données | I | I | **R/A** | — |
| Rapport hebdomadaire GitHub/Jira | **A** | **R** | — | — |
| Rapport mensuel SLA prestataires | **R/A** | C | C | I |
| Négociation renouvellement contrats | **A** | C | — | **R** |
| Escalade incident P1 chez AWS | **A** | **R** | — | C |
| Validation qualité données RTE | **A** | — | **R** | — |

### 4.7 Comités de pilotage prestataires

#### Comité hebdomadaire (Comité Technique)
- **Durée :** 30 minutes
- **Participants :** Chef de projet, DevOps, référent DSI EDF
- **Ordre du jour :** Incidents de la semaine, disponibilité des services, actions correctives
- **Support :** Tableau de bord Grafana + résumé Jira

#### Comité mensuel (Comité de Pilotage)
- **Durée :** 1 heure
- **Participants :** Chef de projet, PO, référent EDF (DSI + Direction R&D)
- **Ordre du jour :** Bilan des KPI projet + prestataires, avancement du sprint en cours, risques, décisions stratégiques
- **Support :** Vue sponsor du tableau de bord (cf. 3.3)

#### Comité de pilotage agile — Conduite de l'équipe

La méthode Scrum intègre nativement la gestion des situations difficiles :

**Gestion des changements de priorité :**
- Toute demande de changement est soumise au PO, qui l'évalue et la positionne dans le backlog
- Les changements urgents (P1) peuvent être intégrés en cours de sprint avec l'accord de l'équipe et en retirant un élément de même taille du sprint en cours
- Règle : **le Sprint Goal est protégé** — pas de modification du sprint backlog sans consensus de l'équipe

**Attribution des rôles en situation d'urgence :**
- En cas d'absence du Scrum Master : Y. Morin → A. Bernard (Data Scientist) prend le relais pour faciliter les Daily Scrums
- En cas d'absence du PO : M. Dupont → Y. Morin assure l'intérim pour les décisions de priorisation urgentes
- En cas d'absence du DevOps (panne critique) : escalade immédiate vers le support AWS (P1) + notification DSI EDF

**Scénarios d'absorption des imprévus :**

| Scénario | Probabilité | Action agile |
|---|---|---|
| Résultats ML décevants sur un modèle | Moyenne | Sprint Review anticipée avec EDF → Ajustement des hyperparamètres → US déplacée au sprint suivant |
| Retard de livraison d'un prestataire (ex : AWS) | Faible | Basculement temporaire sur environnement local Docker → Pas d'impact sur le chemin critique |
| Maladie d'un membre de l'équipe > 3 jours | Moyenne | Repriorisation du Sprint Backlog → US les plus critiques réallouées à 2 personnes au lieu de 1 → Mise à jour du burndown |
| Changement de périmètre demandé par EDF | Faible | Analyse d'impact par le PO → Présentation au Sprint Review → Décision en Sprint Planning suivant |

---

*Document rédigé par l'équipe projet MSPR EDF — Avril 2026*
*Référence : MSPR-TPRE942-B4-L2-v1.0*
