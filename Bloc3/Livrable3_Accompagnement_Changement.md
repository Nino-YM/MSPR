# PLAN D'ACCOMPAGNEMENT DU CHANGEMENT & BONNE UTILISATION DE L'IA
## Projet EDF — Prédiction de la Consommation Électrique Journalière
### MSPR TPRE932 — Bloc de compétences 3 — Livrable 3

---

| Informations document | |
|---|---|
| **Version** | 1.0 |
| **Date** | Avril 2026 |
| **Auteurs** | M. Dupont (Business Analyst / PO), Y. Morin (Chef de projet) |
| **Validé par** | Y. Morin (Chef de projet) |
| **Audience** | Direction EDF, RH, Managers opérationnels, Équipes utilisatrices |

---

## TABLE DES MATIÈRES

1. Analyse d'impact du déploiement IA
2. Stratégie d'accompagnement du changement
3. Kit de bonne utilisation de l'IA
4. Plan d'action synthétique

---

## 1. ANALYSE D'IMPACT DU DÉPLOIEMENT IA

### 1.1 Contexte et périmètre de l'impact

Le déploiement de la solution IA de prédiction de la consommation électrique impacte plusieurs processus existants au sein d'EDF, notamment :
- La **gestion prévisionnelle du mix énergétique** (équilibre production/consommation)
- Les **décisions opérationnelles** des dispatchers et ingénieurs réseau
- Les **processus de reporting** de la Direction R&D et de la Direction Stratégie

L'analyse d'impact porte sur trois dimensions : **processus**, **humain** et **organisationnel**.

### 1.2 Cartographie des processus impactés

| Processus | État avant déploiement IA | État après déploiement IA | Niveau d'impact |
|---|---|---|---|
| **Prévision de consommation journalière** | Modèles statistiques manuels (ARIMA) réalisés par des data analysts — résultats disponibles en J+2 | Prédictions automatiques disponibles en temps réel le matin pour J+1 | Fort |
| **Gestion du mix énergétique** | Répartition production basée sur historiques + expertise humaine | Données IA intégrées comme aide à la décision | Moyen |
| **Reporting direction** | Rapports hebdomadaires manuels | Tableaux de bord automatisés temps réel | Moyen |
| **Maintenance préventive des centrales** | Planification indépendante de la consommation prédite | Synchronisation possible avec les pics de consommation prédits | Faible |
| **Achats d'énergie sur les marchés** | Basé sur les prévisions manuelles | Amélioration de la précision des commandes anticipées | Fort |

### 1.3 Analyse des parties prenantes impactées

| Partie prenante | Rôle | Impact | Niveau de résistance prévisible | Levier d'adhésion |
|---|---|---|---|---|
| **Ingénieurs réseau / Dispatchers** | Utilisateurs directs des prédictions | Fort — changement de l'outil de travail quotidien | Moyen — crainte de remplacer leur expertise | Valorisation de leur rôle d'interprétation et de validation des prédictions IA |
| **Data Analysts EDF** | Anciens producteurs des prévisions manuelles | Fort — leur processus est automatisé | Fort — crainte pour leur emploi | Repositionnement sur l'analyse avancée et l'amélioration des modèles IA |
| **Direction R&D** | Commanditaire du projet | Faible | Très faible — sponsors du projet | Communication des résultats et ROI |
| **Direction des Systèmes d'Information (DSI)** | Intégration technique | Moyen — intégration dans le SI existant | Faible | Implication dès la phase de conception |
| **Acheteurs d'énergie** | Utilisateurs secondaires | Moyen | Faible — gain de précision bienvenu | Démonstration de l'amélioration de la précision (+30 %) |
| **Partenaires RTE** | Fournisseurs de données éco2mix | Faible | Très faible | Communication transparente sur l'usage des données |

### 1.4 Mesure des impacts

#### Impacts positifs attendus

| Impact | Mesure | Gain estimé |
|---|---|---|
| Amélioration de la précision des prévisions | MAPE : de 8 % (ARIMA manuel) à 3,6 % (IA) | **-55 % d'erreur de prédiction** |
| Réduction du temps de production des prévisions | De 2 jours à quelques secondes | **Gain de productivité : ~4h/semaine par data analyst** |
| Réduction des coûts d'achats d'énergie | Meilleure anticipation = moins d'achats d'urgence | **Économie estimée : 2 à 5 M€/an** |
| Amélioration de l'équilibre du réseau | Réduction des écarts production/consommation | Contribution à la sécurité du réseau |

#### Risques liés au changement

| Risque | Probabilité | Impact | Mesure préventive |
|---|---|---|---|
| Résistance au changement des équipes opérationnelles | Moyenne | Élevé | Plan de formation et de communication (cf. section 2) |
| Sur-confiance dans les prédictions IA (désengagement humain) | Faible | Très élevé | Formation sur les limites de l'IA ; maintien d'une validation humaine obligatoire |
| Perte de compétences en modélisation manuelle | Moyenne | Moyen | Maintien de formations sur les méthodes statistiques classiques |
| Refus d'adoption par les utilisateurs (shadow IT) | Faible | Moyen | Implication des utilisateurs clés dès la conception (user stories, tests) |
| Conformité RGPD | Très faible | Élevé | AIPD réalisée, données anonymisées et agrégées |

---

## 2. STRATÉGIE D'ACCOMPAGNEMENT DU CHANGEMENT

La stratégie s'appuie sur le **modèle ADKAR** (Awareness, Desire, Knowledge, Ability, Reinforcement) — référence en conduite du changement.

### 2.1 Phase 1 — AWARENESS : Créer la prise de conscience (Mois 1-2)

**Objectif :** Informer toutes les parties prenantes de l'arrivée de la solution IA et de ses bénéfices.

| Action | Format | Cible | Responsable | Calendrier |
|---|---|---|---|---|
| Lettre de la Direction R&D présentant le projet | Email + PDF | Tous les employés concernés | Direction R&D | Mois 1, Semaine 1 |
| Webinaire de lancement "EDF IA Predict" | Visioconférence (Teams) — 60 min | Tous les managers | Chef de projet | Mois 1, Semaine 2 |
| Article dans la newsletter interne EDF | Newsletter mensuelle | Tous les employés EDF | Communication RH | Mois 2 |
| FAQ disponible sur l'intranet | Page web interne | Tous les employés | BA + Chef de projet | Mois 1, Semaine 3 |

**Messages clés à communiquer :**
- L'IA est un **outil d'aide à la décision**, pas un remplacement des experts humains.
- Les data analysts sont **repositionnés** sur des missions à plus forte valeur ajoutée.
- Les prédictions IA nécessitent **validation et interprétation humaines**.

### 2.2 Phase 2 — DESIRE : Susciter l'envie d'adopter (Mois 2-3)

**Objectif :** Transformer la prise de conscience en volonté d'adoption.

| Action | Format | Cible | Responsable |
|---|---|---|---|
| Démonstration live de la solution IA | Session hands-on (2h) par équipe | Ingénieurs réseau, Data analysts | Data Scientist + BA |
| Témoignages de pairs (early adopters) | Vidéo courte (3 min) diffusée en interne | Tous les utilisateurs | Communication RH |
| Visite du centre de R&D EDF Saclay | Journée de découverte | Managers opérationnels | Chef de projet |
| Sondage interne "Vos attentes vis-à-vis de l'IA" | Questionnaire en ligne (SurveyMonkey) | Tous les utilisateurs | BA |

### 2.3 Phase 3 — KNOWLEDGE : Former les utilisateurs (Mois 3-4)

**Objectif :** Donner aux utilisateurs les connaissances nécessaires pour utiliser la solution correctement.

| Formation | Durée | Format | Cible | Intervenant |
|---|---|---|---|---|
| **Formation A — Comprendre l'IA (Culture IA)** | 3h | Distanciel (e-learning + quiz) | Tous les utilisateurs | Data Scientist |
| **Formation B — Utiliser le dashboard de prédiction** | 4h | Présentiel + exercices pratiques | Ingénieurs réseau, dispatchers | BA + Data Scientist |
| **Formation C — Interpréter les prédictions IA** | 4h | Présentiel | Ingénieurs réseau, acheteurs d'énergie | Data Scientist |
| **Formation D — Administrer et monitorer la solution** | 8h | Hybride (présentiel + TP) | Équipe IT EDF, data analysts | DevOps |
| **Formation E — Gestion des incidents** | 2h | Distanciel | Responsables DSI, référents techniques | DevOps + Chef de projet |

**Évaluation des formations :**
- Test de connaissances avant/après chaque formation (quizz SurveyMonkey)
- Objectif : score post-formation ≥ 80 % pour 100 % des participants
- Certification interne "EDF IA Predict Certified User" délivrée aux participants validés

### 2.4 Phase 4 — ABILITY : Développer les compétences (Mois 4-6)

**Objectif :** Passer de la connaissance théorique à la maîtrise opérationnelle.

| Action | Description | Durée | Responsable |
|---|---|---|---|
| **Pilote accompagné** | Déploiement sur un site pilote (Centre R&D Saclay) avec coaching quotidien | 4 semaines | Chef de projet + Data Scientist |
| **Shadowing** | Les data analysts accompagnent les ingénieurs dans leur utilisation quotidienne de l'outil | 2 semaines | Data analysts |
| **Hotline support** | Numéro de support dédié pendant les 3 premiers mois de déploiement | 3 mois | DevOps + BA |
| **Documentation pratique** | Guide utilisateur illustré (PDF + vidéos tutoriels) disponible sur l'intranet | Permanent | BA |
| **Communauté de pratique** | Canal Teams dédié "EDF IA Predict — Questions & Retours" | Permanent | Chef de projet |

### 2.5 Phase 5 — REINFORCEMENT : Ancrer le changement dans la durée (Mois 6+)

**Objectif :** Pérenniser l'adoption et mesurer le succès du changement.

| Action | Fréquence | Indicateur de succès |
|---|---|---|
| Bilan mensuel d'utilisation (taux d'adoption) | Mensuelle | Taux d'utilisation > 80 % au bout de 3 mois |
| Collecte de feedbacks utilisateurs | Trimestrielle | Score de satisfaction NPS > 7/10 |
| Reconnaissance des "champions IA" (utilisateurs exemplaires) | Semestrielle | Au moins 1 champion identifié par équipe |
| Mise à jour des formations après évolution de l'outil | À chaque nouvelle version | Délai de mise à jour < 2 semaines |
| Revue de la stratégie d'accompagnement | Annuelle | Décision sur les ajustements nécessaires |

---

## 3. KIT DE BONNE UTILISATION DE L'IA

### 3.1 Guide "Comment utiliser les prédictions IA ?"

**À l'attention des ingénieurs réseau et dispatchers EDF**

#### Ce que l'IA fait bien

| Cas d'usage | Précision attendue | Comment l'utiliser |
|---|---|---|
| Prédiction de consommation une journée à l'avance | MAPE ≈ 3,6 % | Utiliser comme référence principale pour la planification J+1 |
| Détection de journées atypiques (canicule, grand froid) | Précision réduite — alerte automatique | Croiser avec les bulletins météo Météo France |
| Tendances saisonnières | Très bonne (été/hiver) | Utile pour la planification de maintenance |

#### Ce que l'IA ne fait pas (limites à connaître)

| Limitation | Raison | Ce que vous devez faire |
|---|---|---|
| Événements exceptionnels imprévus (panne réseau, grève nationale) | Absence de ces événements dans les données d'entraînement | Appliquer votre expertise terrain en complément |
| Données entrantes manquantes ou erronées | Garbage in, garbage out | Vérifier la qualité des données avant de consulter les prédictions |
| Changements réglementaires brusques | Le modèle ne connaît pas les nouvelles règles | Alerter l'équipe Data Science pour un ré-entraînement |
| Prédictions à plus de 3 jours | Trop d'incertitude | Utiliser uniquement les prédictions J+1 (fiabilité maximale) |

#### Processus recommandé — Utilisation quotidienne

```
7h00 — Consultation du dashboard de prédiction
    │
    ├── Prédiction disponible et cohérente avec les tendances historiques ?
    │       │
    │       ├── OUI → Utiliser la prédiction pour planifier le mix énergétique du jour
    │       │
    │       └── NON (écart > 10 % avec J-1 sans raison apparente)
    │                │
    │                ▼
    │           Croiser avec les données météo et l'agenda (férié, événement ?)
    │                │
    │                ├── Écart expliqué → Utiliser la prédiction IA
    │                │
    │                └── Écart inexpliqué → Contacter l'équipe Data Science
    │                                       (canal Teams : EDF IA Predict)
    │
    └── Signaler toute anomalie dans le formulaire de feedback quotidien
```

### 3.2 Check-list d'utilisation responsable de l'IA

Avant de prendre une décision importante basée sur une prédiction IA, cocher les points suivants :

**Vérification de la fiabilité de la prédiction**
- [ ] La prédiction a-t-elle été générée avec des données d'entrée complètes et récentes ?
- [ ] L'indicateur de confiance du modèle est-il dans la plage verte (MAPE < 5 %) ?
- [ ] Y a-t-il une alerte active de dérive du modèle dans le dashboard ?
- [ ] La prédiction est-elle cohérente avec les conditions météo du jour ?
- [ ] Y a-t-il des événements exceptionnels planifiés qui ne sont pas dans les données (panne, événement sportif majeur) ?

**Vérification de la décision**
- [ ] La décision basée sur cette prédiction est-elle réversible facilement si la prédiction est fausse ?
- [ ] Un expert humain a-t-il validé la prédiction avant l'action ?
- [ ] La décision est-elle documentée (avec la prédiction IA utilisée en référence) ?

**Signalement**
- [ ] En cas d'écart constaté entre prédiction et réalité > 10 %, le formulaire de feedback a-t-il été complété ?

### 3.3 Outils de type Lean Management — Amélioration continue

#### A. Formulaire de feedback quotidien (KAIZEN)

Accessible depuis le dashboard IA via le bouton "Signaler un écart" :

```
┌─────────────────────────────────────────────────────────┐
│         FORMULAIRE DE FEEDBACK — EDF IA PREDICT         │
├─────────────────────────────────────────────────────────┤
│ Date : ___/___/______   Heure : _____                   │
│                                                         │
│ Prédiction IA (MW) : _________                          │
│ Consommation réelle (MW) : _________                    │
│ Écart (%) : _________                                   │
│                                                         │
│ Type d'écart :                                          │
│   □ Événement météo imprévu                             │
│   □ Événement calendaire manquant (férié, événement)    │
│   □ Anomalie technique (données manquantes)             │
│   □ Autre : _________________________________           │
│                                                         │
│ Impact opérationnel :                                   │
│   □ Faible (< 0,5 % d'écart sur le réseau)             │
│   □ Moyen (0,5 % à 2 %)                                 │
│   □ Fort (> 2 %)                                        │
│                                                         │
│ Action corrective prise : _____________________________ │
│                                                         │
│ Nom : ________________   Équipe : ________________      │
└─────────────────────────────────────────────────────────┘
```

Ces feedbacks sont analysés **hebdomadairement** par le Data Scientist pour identifier les patterns d'erreurs et améliorer les modèles.

#### B. Tableau A3 — Amélioration continue (Résolution de problèmes)

Le tableau A3 est un outil Lean standardisé pour traiter un problème de manière structurée. À utiliser pour tout écart de prédiction récurrent :

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TABLEAU A3 — AMÉLIORATION CONTINUE                   │
│                    Problème : Écart de prédiction récurrent             │
├────────────────────┬────────────────────────────────────────────────────┤
│ 1. CONTEXTE        │ Description du problème et de son importance       │
│                    │ Ex : Prédiction systématiquement sous-estimée      │
│                    │ les lundis en janvier (écart moyen : +8 %)         │
├────────────────────┼────────────────────────────────────────────────────┤
│ 2. SITUATION       │ Données quantifiées du problème                    │
│ ACTUELLE          │ Graphique MAPE par jour de la semaine               │
├────────────────────┼────────────────────────────────────────────────────┤
│ 3. ANALYSE DES     │ Méthode des 5 Pourquoi :                           │
│ CAUSES            │ Pourquoi ? Données insuffisantes pour lundi matin  │
│                    │ Pourquoi ? Comportement atypique post-week-end     │
│                    │ Pourquoi ? Variable "reprise travail" manquante    │
├────────────────────┼────────────────────────────────────────────────────┤
│ 4. OBJECTIF        │ MAPE < 4 % pour les lundis en janvier              │
├────────────────────┼────────────────────────────────────────────────────┤
│ 5. PLAN D'ACTION   │ Ajouter la variable "J+1 est lundi" comme feature  │
│                    │ Ré-entraîner le modèle                             │
│                    │ Valider sur les lundis de 2024                     │
├────────────────────┼────────────────────────────────────────────────────┤
│ 6. RÉSULTATS       │ MAPE lundis janvier après correction : 3,2 %       │
├────────────────────┼────────────────────────────────────────────────────┤
│ 7. CAPITALISATION  │ Documentation de la feature ajoutée                │
│                    │ Partage en réunion mensuelle de l'équipe           │
└────────────────────┴────────────────────────────────────────────────────┘
```

#### C. Réunion mensuelle d'amélioration continue

**Format :** 1h, présentiel ou Teams, le dernier jeudi de chaque mois

| Point | Durée | Animateur | Contenu |
|---|---|---|---|
| Bilan des prédictions du mois | 15 min | Data Scientist | R², MAPE, RMSE, tendances |
| Analyse des feedbacks utilisateurs | 15 min | BA | Principaux écarts signalés |
| Points bloquants / incidents | 10 min | DevOps | Incidents et résolutions |
| Actions d'amélioration | 15 min | Tous | Priorisation des actions A3 |
| Questions libres | 5 min | Chef de projet | Ouverte à tous |

---

## 4. PLAN D'ACTION SYNTHÉTIQUE

### 4.1 Calendrier global d'accompagnement

| Mois | Phase ADKAR | Actions clés | Responsable |
|---|---|---|---|
| M1 | Awareness | Lettre direction, webinaire lancement, FAQ intranet | Chef de projet |
| M2 | Awareness + Desire | Newsletter, démonstrations live, sondage | BA + Data Scientist |
| M3 | Desire + Knowledge | Formations A, B, C | Data Scientist + BA |
| M4 | Knowledge + Ability | Formations D, E, déploiement pilote (Saclay) | DevOps + BA |
| M5 | Ability | Shadowing, hotline, communauté de pratique | Équipe projet |
| M6 | Reinforcement | Bilan pilote, ajustements, généralisation | Chef de projet |
| M7-12 | Reinforcement | Bilans mensuels, feedbacks, champions IA | Chef de projet + BA |

### 4.2 Indicateurs de succès de l'accompagnement

| KPI | Cible | Méthode de mesure | Fréquence |
|---|---|---|---|
| Taux de participation aux formations | 100 % | Liste de présence | Par session |
| Score moyen aux quiz de formation | ≥ 80 % | Quiz SurveyMonkey | Par session |
| Taux d'adoption du dashboard IA | ≥ 80 % à M+3 | Logs d'accès à la plateforme | Mensuelle |
| Nombre de feedbacks soumis | ≥ 2/semaine/équipe | Formulaire de feedback | Hebdomadaire |
| Score de satisfaction utilisateurs (NPS) | ≥ 7/10 | Enquête trimestrielle | Trimestrielle |
| Taux d'incidents liés à une mauvaise utilisation | 0 | Analyse des incidents | Continue |

### 4.3 Budget d'accompagnement

| Poste de dépense | Budget alloué | Détail |
|---|---|---|
| Formations (conception + animation) | 8 000 € | 5 formations × 1 600 € moyen |
| Supports de communication (intranet, vidéos) | 3 000 € | Production vidéo, rédaction |
| Hotline support (3 mois) | 5 000 € | 2h/jour × 65 jours × 40 €/h |
| Réunions d'amélioration continue (12 mois) | 2 000 € | Salle, déplacements |
| Contingence | 2 000 € | 10 % |
| **Total** | **20 000 €** | |

---

*Document rédigé par l'équipe projet MSPR EDF — Avril 2026*
*Référence : MSPR-TPRE932-B3-L3-v1.0*
