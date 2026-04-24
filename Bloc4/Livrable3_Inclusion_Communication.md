# PLAN D'INCLUSION, DE COMMUNICATION & DE COLLABORATION D'ÉQUIPE
## Projet EDF — Prédiction de la Consommation Électrique Journalière
### MSPR TPRE942 — Bloc de compétences 4 — Livrable 3

---

| Informations document | |
|---|---|
| **Version** | 1.0 |
| **Date** | Avril 2026 |
| **Auteurs** | Y. Morin (Chef de projet), M. Dupont (Business Analyst) |
| **Contexte** | Projet international EDF — équipes France + R&D Chine, UK, Allemagne, Italie |

---

## TABLE DES MATIÈRES

1. Stratégie d'accueil et d'inclusion des handicaps
2. Communication interculturelle et prévention des conflits
3. Processus de communication inclusif et réunions à distance

---

## 1. STRATÉGIE D'ACCUEIL ET D'INCLUSION DES HANDICAPS

### 1.1 Cadre légal et engagement EDF

EDF est soumis à l'obligation d'emploi de travailleurs handicapés (OETH) — loi du 10 juillet 1987, modifiée par la loi du 11 février 2005 pour l'égalité des droits et des chances. EDF s'engage à employer au minimum 6 % de personnes en situation de handicap.

Le déploiement du projet IA de prédiction intègre dès sa conception une démarche d'inclusion totale, en lien avec :
- Le **référent handicap EDF** (Mission Handicap EDF)
- Les principes **AGEFIPH** (Association de Gestion du Fonds pour l'Insertion Professionnelle des Handicapés)
- Les normes **WCAG 2.1** (accessibilité numérique) pour les interfaces utilisateurs

### 1.2 Les 6 grandes familles de handicap (AGEFIPH)

L'AGEFIPH recense 6 grandes familles de handicap que notre équipe doit connaître et prendre en compte :

#### Famille 1 — Handicap MOTEUR

**Description :** Difficultés à se déplacer, à effectuer certains gestes, ou à utiliser les membres supérieurs. Inclut les personnes en fauteuil roulant, les personnes avec une mobilité réduite des bras ou des mains (ex : hémiplégie, paraplégie, myopathie).

**Exemples concrets :** Difficulté à taper au clavier, à utiliser une souris standard, à rester assis longtemps.

**Adaptations dans le projet :**
- Accès aux réunions à distance depuis tout lieu adapté (Teams — pas de déplacement obligatoire)
- Utilisation de logiciels de contrôle vocal (Dragon NaturallySpeaking) pour la rédaction de documents
- Envoi des supports de réunion 48h à l'avance pour permettre la lecture en amont sans prise de note simultanée
- Clavier ergonomique, souris trackball ou tablette graphique selon les besoins
- Pauses planifiées lors des sessions de travail intensif (toutes les 90 minutes maximum)
- Adaptation du poste de travail en coordination avec le référent handicap EDF et la médecine du travail

#### Famille 2 — Handicap SENSORIEL : Visuel

**Description :** Déficiences visuelles allant de la malvoyance à la cécité totale. Inclut les daltoniens.

**Exemples concrets :** Incapacité à lire les petits textes, impossibilité d'utiliser une interface graphique standard, difficulté avec les graphiques en couleur.

**Adaptations dans le projet :**
- Interfaces et dashboards conformes aux normes WCAG 2.1 niveau AA (contraste de couleur ≥ 4,5:1)
- Utilisation de lecteurs d'écran (NVDA, JAWS) — l'API FastAPI génère des réponses JSON accessibles
- Palette de couleurs accessible pour les daltoniens (éviter rouge/vert pour les indicateurs — utiliser formes + couleurs)
- Documents texte fournis en complément de tout document contenant des graphiques
- Taille de police minimale 12pt dans tous les documents partagés
- Support en format audio (enregistrements Teams) de toutes les réunions importantes
- Alternatives textuelles (alt text) à toutes les images dans les présentations et la documentation

#### Famille 3 — Handicap SENSORIEL : Auditif

**Description :** Difficultés ou impossibilité d'entendre. Inclut les sourds de naissance et les malentendants.

**Exemples concrets :** Impossibilité de participer à une réunion audio, difficulté à entendre en visioconférence dans un environnement bruyant.

**Adaptations dans le projet :**
- Activation systématique des **sous-titres automatiques** sur Teams lors de toutes les réunions
- Interprétariat en **Langue des Signes Française (LSF)** pour les événements importants (formations, Sprint Reviews avec EDF)
- **Compte-rendu écrit intégral** de chaque réunion posté dans le canal Teams dédié (format texte, pas seulement audio/vidéo)
- Communication écrite favorisée (Teams, email) en complément des échanges oraux
- Fichiers de transcription automatique (Teams Transcription) systématiquement activés
- **Politique "chat en parallèle"** : pendant les réunions Teams, le canal de chat est actif pour que les personnes malentendantes puissent suivre et intervenir par écrit

#### Famille 4 — Handicap PSYCHIQUE

**Description :** Troubles psychiques pouvant affecter le comportement et les relations au travail : troubles anxieux, dépression, troubles bipolaires, schizophrénie. Distinct du handicap mental.

**Exemples concrets :** Difficulté à gérer le stress, la pression des délais, les situations de conflit, les environnements bruyants ou trop stimulants.

**Adaptations dans le projet :**
- **Charge de travail prévisible** : planning partagé en avance (Jira + calendrier Teams), pas de demandes urgentes de dernière minute
- **Flexibilité horaire** : accord de télétravail flexible, horaires aménagés selon les besoins
- **Communication bienveillante** : pas de reproche public, feedback toujours donné en privé en premier
- **Processus de signalement sécurisé** : ligne directe confidentielle avec le référent handicap EDF
- **Droit à la déconnexion** : aucune notification Teams en dehors de 9h-18h sauf urgence P1
- **Réunions structurées** : ordre du jour envoyé 48h à l'avance, durée respectée strictement
- **Soutien pairs** : binôme de soutien identifié pour chaque membre (buddy system)
- Accès facilité au service d'Assistance aux Employés (EAP — Employee Assistance Program) EDF

#### Famille 5 — Handicap MENTAL (Cognitif)

**Description :** Déficiences intellectuelles affectant les capacités d'apprentissage, de compréhension et d'adaptation. Distinct du handicap psychique.

**Exemples concrets :** Difficultés avec les instructions complexes, les tâches longues multi-étapes, la gestion du temps.

**Adaptations dans le projet :**
- Documentation rédigée en **"FALC"** (Facile à Lire et à Comprendre) pour les guides utilisateurs destinés aux employés EDF non-techniques
- **Instructions décomposées** : toute tâche complexe est décomposée en micro-tâches dans Jira
- **Tutoriels visuels** : vidéos de formation avec sous-titres et visuels simples (pas uniquement du texte)
- **Répétition et révision** : fiches mémo plastifiées des procédures clés mis à disposition
- Vérification régulière de la compréhension (pas d'assomption que "c'est compris")
- Accès à un référent dédié pour toute question, sans jugement

#### Famille 6 — Handicap INVALIDANT (Maladies invalidantes)

**Description :** Maladies chroniques ou invalidantes limitant les capacités de travail : cancer, maladies cardiaques, diabète, maladies auto-immunes, épilepsie, etc.

**Exemples concrets :** Fatigue chronique imposant des limites sur les horaires, contraintes médicales (prises de médicaments, consultations), périodes de traitement.

**Adaptations dans le projet :**
- **Aménagement du temps de travail** : mi-temps thérapeutique possible pendant les périodes de traitement
- **Télétravail complet** : accessible à tout moment sur justificatif médical, sans nécessiter de justification détaillée
- **Gestion de l'absentéisme prévisible** : les périodes de traitement connues à l'avance sont intégrées dans le planning Scrum (vélocité ajustée)
- **Confidentialité médicale absolue** : seul le référent handicap connaît la nature du handicap — l'équipe sait uniquement les aménagements nécessaires
- **Continuité des missions** : un backup est désigné pour chaque mission critique afin de garantir la continuité en cas d'absence

### 1.3 Articulation avec le référent handicap EDF

Le **référent handicap EDF** (Mission Handicap EDF) est le point de contact central pour tous les aménagements liés au handicap.

**Processus d'aménagement du poste :**

```
[Employé ou manager identifie un besoin d'aménagement]
                │
                ▼
[Échange confidentiel avec le référent handicap EDF]
                │
                ▼
[Évaluation des besoins avec la médecine du travail]
                │
                ▼
[Définition des aménagements (matériels, organisationnels, temporels)]
                │
                ▼
[Mise en place des aménagements (financement AGEFIPH si applicable)]
                │
                ▼
[Suivi et ajustement trimestriel]
```

**Engagements de l'équipe projet :**
- Présenter les 6 familles de handicap lors du kick-off (15 minutes)
- Inclure une clause d'inclusion dans le contrat d'équipe (Team Charter)
- Signaler systématiquement les besoins d'aménagement au référent handicap dès leur identification
- Réaliser un audit d'accessibilité de tous les livrables numériques avant livraison à EDF

### 1.4 Règles et bonnes pratiques d'inclusion dans le projet

| Domaine | Règle | Outil / Méthode |
|---|---|---|
| **Réunions** | Ordre du jour systématique 48h avant | Teams Calendar |
| **Documents** | Format accessible (police 12pt min, contraste ≥ 4,5:1) | Word Accessibilité Checker |
| **Réunions Teams** | Sous-titres activés par défaut | Paramètres Teams |
| **Vidéos de formation** | Sous-titres systématiques | Teams + sous-titrage auto |
| **Dashboards** | Palette accessible daltoniens | WCAG 2.1 |
| **Charge de travail** | Pas de réunion > 2h sans pause | Règle d'équipe |
| **Communication** | Pas de message Teams après 18h | Paramètres de notification |
| **Absentéisme** | Backup désigné pour chaque rôle critique | Team Charter |

---

## 2. COMMUNICATION INTERCULTURELLE & PRÉVENTION DES CONFLITS

### 2.1 Contexte international du projet EDF

Le projet implique des parties prenantes réparties sur plusieurs sites EDF à l'international :

| Site EDF | Pays | Fuseau horaire | Rôle dans le projet |
|---|---|---|---|
| **EDF Saclay / Paris** | France | UTC+1 (UTC+2 en été) | Équipe projet principale, commanditaire |
| **EDF R&D London** | Royaume-Uni | UTC+0 (UTC+1 en été) | Expertise en ML et Smart Grids |
| **EDF R&D Shanghai** | Chine | UTC+8 | Expertise en prédiction de consommation |
| **EDF R&D Aachen** | Allemagne | UTC+1 (UTC+2 en été) | Expertise en réseaux de distribution |
| **EDF R&D Roma** | Italie | UTC+1 (UTC+2 en été) | Expertise en énergies renouvelables |

### 2.2 Modes de communication adaptés aux cultures et fuseaux horaires

#### Carte des cultures (modèle de Hofstede appliqué)

| Pays | Distance hiérarchique | Individualisme | Evitement de l'incertitude | Points clés |
|---|---|---|---|---|
| **France** | Élevée | Élevé | Élevé | Communication directe mais hiérarchique ; formalisme dans les réunions |
| **Royaume-Uni** | Faible | Très élevé | Faible | Humour indirect ; understatement ; pragmatisme ; flexibilité |
| **Chine** | Très élevée | Faible (collectiviste) | Moyen | "Face" (mianzi) = ne pas mettre en difficulté en public ; consensus de groupe |
| **Allemagne** | Faible | Élevé | Très élevé | Ponctualité absolue ; préparation rigoureuse des réunions ; directivité |
| **Italie** | Moyenne | Élevé | Élevé | Importance des relations personnelles ; flexibilité sur les délais ; expressivité |

#### Règles de communication adaptées par culture

**Avec les collègues britanniques :**
- Utiliser l'anglais comme langue de travail — éviter les expressions trop françaises
- L'understatement est courant : "That's quite interesting" peut signifier une réserve. Demander des précisions.
- Les critiques sont formulées indirectement : écoute attentive entre les lignes
- Humour bienvenu — créer une atmosphère détendue favorise la collaboration

**Avec les collègues chinois :**
- **Ne jamais critiquer publiquement** un collègue ou un résultat de leur équipe en réunion → toujours faire le feedback en privé d'abord
- Le silence n'est pas un désaccord — c'est souvent du respect ou de la réflexion
- Les décisions prennent plus de temps (consensus collectif) — anticiper des délais plus longs pour les validations
- Fêtes importantes à respecter : Nouvel An Chinois (janvier-février) → prévoir les livrables en conséquence
- Formule de politesse en début de réunion en mandarin (effort apprécié) : "Nǐ hǎo" (bonjour)

**Avec les collègues allemands :**
- La ponctualité est une marque de respect absolu — commencer les réunions à l'heure exacte, toujours
- Préparer des présentations très structurées avec des données chiffrées — les décisions se basent sur les faits
- Les questions peuvent sembler "agressives" — c'est une culture de la rigueur, pas du conflit
- Titres académiques importants : s'adresser à un Dokteur par son titre jusqu'à invitation à la familiarité

**Avec les collègues italiens :**
- Les relations personnelles comptent autant que les relations professionnelles — investir du temps informel
- La ponctualité est plus flexible — ne pas s'offusquer d'un léger retard (5-10 min)
- Les discussions peuvent être animées et expressives — ce n'est pas un conflit
- Le "non" direct est rare — apprendre à lire les signaux indirects d'un désaccord

#### Gestion des fuseaux horaires

| Plage horaire (heure Paris) | Sites disponibles | Usage recommandé |
|---|---|---|
| **9h00 - 10h30** | France, UK, Allemagne, Italie | Réunions Europe : Sprint Reviews, Comités |
| **14h00 - 15h30** | France, UK, Allemagne, Italie, Chine (21h-22h30 à Shanghai) | Réunions incluant la Chine (ponctuelles — pas régulières) |
| **16h00 - 18h00** | France, UK, Allemagne, Italie | Plage de travail collaboratif Europe |

**Règle d'or :** Aucune réunion obligatoire avant 9h ou après 18h heure locale des participants. Les réunions avec la Chine sont planifiées en rotation pour alterner l'inconfort horaire.

### 2.3 Exemples de malentendus multiculturels et stratégies de résolution

#### Malentendu 1 — Le silence chinois interprété comme un accord

**Situation :** Lors d'une Sprint Review avec le centre de R&D de Shanghai, l'équipe présente le choix du modèle Random Forest. Aucun commentaire de l'équipe chinoise. L'équipe française interprète cela comme une validation.

**Réalité :** L'équipe chinoise avait des réserves mais n'a pas voulu les exprimer publiquement pour ne pas perdre la face.

**Stratégie de résolution :**
1. Envoyer un email de suivi après chaque réunion : "Suite à notre appel, pouvez-vous confirmer votre accord ou partager vos commentaires d'ici vendredi ?"
2. Prévoir des échanges bilatéraux privés avec le responsable chinois avant les grandes réunions
3. Désigner un "cultural liaison" dans l'équipe (quelqu'un ayant de l'expérience avec la culture chinoise)

#### Malentendu 2 — La directivité allemande perçue comme de l'agressivité

**Situation :** Un ingénieur du centre de R&D d'Aachen envoie un email très direct : "Votre modèle RBF est insuffisant. La documentation est incomplète. Nous attendons une correction sous 24h."

**Réalité :** C'est un style de communication normal en Allemagne — factuel, direct, sans formules de politesse superflues. Ce n'est pas du mépris.

**Stratégie de résolution :**
1. Répondre sur le même registre factuel, sans se mettre en défensif
2. Traiter les points soulevés comme des contributions constructives
3. Former l'équipe sur le style de communication allemand dès le kick-off (30 min de sensibilisation)

#### Malentendu 3 — La flexibilité italienne perçue comme du désengagement

**Situation :** L'équipe italienne de R&D de Rome ne répond pas aux emails en moins de 48h et est souvent en retard dans les livrables documentaires.

**Réalité :** La culture italienne valorise les relations directes et les échanges verbaux — les emails sont moins prioritaires que les appels.

**Stratégie de résolution :**
1. Préférer les appels Teams aux emails pour les sujets urgents
2. Reconfirmer les délais lors des appels (et non par email uniquement)
3. Accepter une légère flexibilité sur les délais documentaires tout en maintenant la fermeté sur les livrables critiques (chemin critique)

### 2.4 Solutions innovantes pour favoriser les interactions et prévenir les conflits

#### Solution 1 — Serious Game à distance : "Culture Quest EDF"

**Format :** Session de 90 minutes en ligne (Teams + Klaxoon), au début du projet et après chaque recrutement

**Contenu :** Jeu de quizz interactif sur les cultures des pays impliqués dans le projet (traditions, valeurs, communication). Les équipes sont mélangées (France + international) pour favoriser l'apprentissage par l'échange.

**Objectif :** Déconstruire les stéréotypes, créer une culture d'équipe commune, rire ensemble.

**Outil :** Klaxoon (quiz interactif) + Teams (vidéo)

#### Solution 2 — Temps de partage informel : "EDF Coffee Break Virtuel"

**Format :** 30 minutes de café informel en visioconférence, 1 fois par semaine, sans ordre du jour

**Règles :**
- Pas de sujets professionnels obligatoires
- Rotation du pays "hôte" (partage d'une recette, d'une tradition, d'une musique)
- Caméra allumée recommandée (mais pas obligatoire pour favoriser l'inclusion des personnes avec des contraintes)

**Objectif :** Créer des liens humains au-delà des fuseaux horaires, prévenir l'isolement en télétravail.

**Planification :** Mardi, 14h30 heure Paris (accessible France + UK + Allemagne + Italie + Chine en soirée, rotation)

#### Solution 3 — Webinaire interculturel : "Cultures & Collaboration chez EDF"

**Format :** Webinaire de 2 heures, animé par un intervenant spécialiste en communication interculturelle (cabinet externe)

**Programme :**
- Module 1 (45 min) : Les 5 dimensions culturelles de Hofstede appliquées à EDF
- Module 2 (45 min) : Simulations de situations de malentendu interculturel + débriefing
- Module 3 (30 min) : Construction d'un "Team Charter" interculturel commun

**Fréquence :** Au démarrage du projet, puis une fois par an

**Coût estimé :** 1 500 à 2 500 € pour un cabinet spécialisé (ex : Berlitz Corporate, Orange Mélodie Consulting)

#### Solution 4 — Webinaire "Ressources numériques & Handicap"

**Format :** Session de 1 heure (Teams), animée par le référent handicap EDF

**Programme :**
- Présentation des 6 familles de handicap AGEFIPH (20 min)
- Démonstration des outils d'accessibilité disponibles : lecteurs d'écran, sous-titres Teams, logiciels de contrôle vocal (20 min)
- Questions / Réponses et engagement de l'équipe (20 min)

**Objectif :** Sensibiliser tous les membres de l'équipe projet (y compris les sites internationaux) aux enjeux d'inclusion numérique

**Fréquence :** Une fois par an et à chaque intégration d'un nouveau membre

---

## 3. PROCESSUS DE COMMUNICATION INCLUSIF & RÉUNIONS À DISTANCE

### 3.1 Architecture de communication du projet

```
╔══════════════════════════════════════════════════════════════════════╗
║              SCHÉMA DE COMMUNICATION — PROJET EDF IA PREDICT        ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  NIVEAU STRATÉGIQUE (Mensuel)                                        ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ Comité de pilotage (Chef de projet + Direction EDF)             │ ║
║  │ Outil : Teams + PowerPoint + Tableau de bord sponsor            │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                          │                                           ║
║                          ▼                                           ║
║  NIVEAU PROJET (Par sprint / Bihebdo)                                ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ Sprint Review (Équipe + PO + Stakeholders EDF)                  │ ║
║  │ Sprint Retrospective (Équipe uniquement)                        │ ║
║  │ Backlog Refinement (PO + Scrum Master + Équipe)                 │ ║
║  │ Outil : Teams + Jira + Confluence                               │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                          │                                           ║
║                          ▼                                           ║
║  NIVEAU OPÉRATIONNEL (Quotidien)                                     ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ Daily Scrum (Équipe de développement — 15 min)                  │ ║
║  │ Check-in / Check-out Teams (canal #daily-standup)               │ ║
║  │ Fil de discussion Teams par thématique                          │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 3.2 Adaptabilité des outils pour les collaborateurs en situation de handicap

| Outil | Utilisation principale | Accessibilité native | Alternative pour collaborateurs en situation de handicap |
|---|---|---|---|
| **Microsoft Teams** | Communication, réunions | Sous-titres auto, contraste élevé, navigation clavier | Sous-titres LSF (Leinahtan, prestataire) pour personnes sourdes ; mode "text only" pour malvoyants |
| **Jira** | Gestion du backlog | Partiellement accessible | Résumé hebdomadaire Jira envoyé par email en format texte brut |
| **Confluence** | Documentation | Accessible aux lecteurs d'écran | Documents également disponibles en Word accessible (.docx) |
| **Grafana** | Monitoring | Palette de couleurs paramétrable | Tableau de données en complément de chaque graphique ; export CSV |
| **Klaxoon** | Animations interactives | Navigation clavier | Accès téléphone (audio) si contrainte visuelle |
| **Email** | Communication formelle | Universellement accessible | Format alternatif disponible sur demande |

**Politique "No Tool Left Behind" :** Avant tout déploiement d'un nouvel outil numérique dans le projet, le chef de projet vérifie son niveau d'accessibilité (test WAVE ou équivalent) et identifie une alternative pour les membres de l'équipe qui ne pourraient pas l'utiliser.

### 3.3 Fil de discussion — Processus de check-in / check-out

**Objectif :** Maintenir le lien social et la synchronisation quotidienne de l'équipe, y compris pour les membres en télétravail ou à distance internationale.

**Structure du fil de discussion (canal Teams : `#daily-standup`)** :

```
─────────────── Lundi 14 avril 2026 ───────────────

🟢 CHECK-IN — A. Bernard (Data Scientist) — 9h12
✅ Hier : Finalisation de l'implémentation du modèle Random Forest.
   R² = 0,95 sur le jeu de test — objectif atteint !
🎯 Aujourd'hui : Évaluation comparative des 4 modèles + préparation graphiques Sprint Review.
🚧 Blocages : Aucun.

🟢 CHECK-IN — C. Nguyen (DevOps) — 9h24
✅ Hier : Dockerfile finalisé, tests locaux OK.
🎯 Aujourd'hui : Configuration GitHub Actions pour le pipeline CI/CD.
🚧 Blocages : Besoin des credentials AWS ECR → @Y. Morin peux-tu partager via Secrets Manager ?

🟢 CHECK-IN — M. Dupont (PO) — 9h31
✅ Hier : Réunion avec référent EDF — validation des US01, US02, US06.
🎯 Aujourd'hui : Mise à jour du backlog Jira + rédaction des critères d'acceptation US03.
🚧 Blocages : Aucun.

🟢 CHECK-IN — Y. Morin (Chef de projet / SM) — 9h33
✅ Hier : Coordination Sprint Planning S3 + mise à jour tableau de bord sponsor.
🎯 Aujourd'hui : Fourniture des credentials AWS à C. Nguyen + facilitation Daily 15 min.
🚧 Blocages : Aucun.

─────────────── Soir ───────────────

🔵 CHECK-OUT — A. Bernard — 17h55
📊 Avancement : Évaluation comparative terminée à 90 % (manque graphiques MAPE).
📝 Note : Random Forest clairement le meilleur — présentation Sprint Review prête pour vendredi.

🔵 CHECK-OUT — C. Nguyen — 18h01
📊 Avancement : GitHub Actions configuré — premier pipeline vert en CI ✅.
📝 Note : Tests de charge (Locust) à lancer demain matin.
```

### 3.4 Kit de réunion à distance — Sprint Review (exemple complet)

La Sprint Review est la cérémonie la plus importante pour les stakeholders EDF. Voici un kit complet pour l'animer efficacement à distance.

#### Structure type d'une Sprint Review (1 heure)

| Phase | Durée | Animateur | Contenu | Outil |
|---|---|---|---|---|
| **Ouverture** | 5 min | Scrum Master | Rappel de l'ordre du jour, des participants, des règles (caméra recommandée, chat actif, questions en fin) | Teams |
| **Rappel du Sprint Goal** | 3 min | Scrum Master | Rappel de l'objectif du sprint et des User Stories planifiées | PowerPoint |
| **Démonstration des fonctionnalités** | 25 min | Équipe de développement | Demo live de chaque US terminée (pas de slides — application réelle) | Partage d'écran Teams |
| **Séance de Q&R et feedback** | 15 min | PO (facilitation) | Questions des stakeholders EDF ; feedback sur les fonctionnalités démontrées | Chat Teams + parole |
| **Revue du Backlog** | 5 min | PO | Présentation du backlog actualisé, teaser du prochain sprint | Jira partagé à l'écran |
| **Clôture** | 7 min | Scrum Master | Récap des décisions, des actions ; sondage de satisfaction (Klaxoon) | Klaxoon + Teams |

#### Bonnes pratiques pour maintenir la dynamique de groupe à distance

| Pratique | Description | Fréquence |
|---|---|---|
| **Caméra recommandée (mais pas obligatoire)** | La caméra maintient l'engagement — mais l'accessibilité prime (handicap, contrainte technique) | Toutes les réunions |
| **Répartition équitable de la parole** | Le Scrum Master veille à ce que chaque participant ait la parole au moins une fois par réunion | Toutes les réunions |
| **Sondage interactif d'ouverture** | Klaxoon — question brise-glace pour activer l'attention dès le début | Sprint Review, formations |
| **Chat en parallèle** | Le canal chat Teams est actif pendant toute la réunion pour permettre aux participants qui ne prennent pas la parole de contribuer par écrit | Toutes les réunions |
| **Pause** | Pour toute réunion > 60 minutes : pause de 10 minutes à mi-parcours | Formations, ateliers |
| **Enregistrement disponible** | Toutes les Sprint Reviews sont enregistrées et partagées dans le canal Teams pour les absents ou les malentendants | Sprint Reviews |
| **Résumé post-réunion** | Compte-rendu structuré posté dans Teams dans les 2h après la réunion | Toutes les cérémonies |
| **Temps de parole en anglais disponible** | Pour les participants internationaux (UK, Chine, Allemagne, Italie), un résumé en anglais est fourni en fin de réunion si la réunion s'est tenue en français | Sprint Reviews internationales |

#### Outils digitaux d'animation utilisés

| Outil | Usage | Accessibilité handicap |
|---|---|---|
| **Klaxoon** | Quizz interactifs, votes, sondages, brainstorming virtuel (Post-its numériques) | Navigation clavier disponible ; alternative texte fournie |
| **Kahoot** | Quizz de vérification des connaissances lors des formations | Sous-titres si audio, grand contraste disponible |
| **Padlet** | Tableau blanc collaboratif pour rétrospectives Scrum (Start/Stop/Continue) | Version texte disponible en parallèle |
| **Mentimeter** | Nuages de mots, sondages en temps réel pour les décisions collectives | Accessible clavier et lecteur d'écran |
| **Microsoft Whiteboard** | Tableau blanc intégré à Teams pour les ateliers de conception | Accessible aux utilisateurs de Teams avec navigation clavier |

#### Adaptations pour les 6 familles de handicap en réunion à distance

| Famille | Adaptation spécifique lors des réunions |
|---|---|
| **Moteur** | Commandes vocales Teams activées ; durée de réunion limitée à 90 min avec pause obligatoire ; envoi du support 48h avant pour éviter la prise de note simultanée |
| **Visuel** | Descriptions verbales de tous les visuels présentés ("Le graphique montre une courbe descendante...") ; pas de contenu uniquement en image |
| **Auditif** | Sous-titres Teams activés ; interprète LSF disponible sur demande ; chat Teams actif pour questions écrites ; enregistrement + transcription fournis |
| **Psychique** | Ordre du jour fourni 48h avant ; aucune improvisation ; no-interruption rules ; droit de se déconnecter si besoin sans justification |
| **Mental** | Reformulations régulières des points clés ; questions posées une par une, pas de rapidité imposée ; résumé visuel simplifié fourni après la réunion |
| **Invalidant** | Flexibilité totale sur la présence caméra ; possibilité de participer uniquement à une partie de la réunion ; résumé complet fourni après |

### 3.5 Processus de résolution des conflits

En cas de conflit au sein de l'équipe ou avec les parties prenantes EDF, le processus suivant est appliqué :

```
NIVEAU 1 — Résolution directe
Les parties concernées s'entretiennent en privé pour trouver une solution.
Délai : 48h maximum.

        │ Si échec
        ▼

NIVEAU 2 — Médiation par le Scrum Master
Y. Morin (Scrum Master) organise une session de médiation.
Écoute active, reformulation, recherche de compromis.
Délai : 1 semaine maximum.

        │ Si échec
        ▼

NIVEAU 3 — Escalade vers le Product Owner
M. Dupont (PO) arbitre en prenant la décision de priorité côté produit.
Pour les conflits interpersonnels : escalade vers les RH EDF.

        │ Si échec
        ▼

NIVEAU 4 — Escalade vers la Direction EDF
Arbitrage par le commanditaire EDF (Direction R&D).
```

---

## ANNEXE — Résumé des engagements d'inclusion de l'équipe (Team Charter)

*Document signé par tous les membres de l'équipe en séance de kick-off*

```
CHARTE D'ÉQUIPE — EDF IA PREDICT
Engagement collectif d'inclusion et de collaboration

NOUS NOUS ENGAGEONS À :

✅ Respecter les fuseaux horaires de tous les membres (pas de réunion avant 9h ni après 18h heure locale)
✅ Activer les sous-titres Teams pour toutes nos réunions
✅ Fournir les ordres du jour 48h à l'avance
✅ Communiquer en anglais lors des échanges avec les sites internationaux
✅ Ne jamais critiquer publiquement un collègue — le feedback se fait en privé d'abord
✅ Respecter les adaptations nécessaires pour les collègues en situation de handicap
✅ Rédiger un résumé écrit après chaque réunion importante
✅ Appliquer la règle "No Tool Left Behind" pour tout nouvel outil numérique
✅ Signaler tout conflit au Scrum Master dès son émergence, sans attendre
✅ Prendre soin de notre bien-être et signaler toute difficulté sans crainte de jugement

Signatures : Y. Morin, A. Bernard, C. Nguyen, M. Dupont
Date de signature : [Date du kick-off]
```

---

*Document rédigé par l'équipe projet MSPR EDF — Avril 2026*
*Référence : MSPR-TPRE942-B4-L3-v1.0*
