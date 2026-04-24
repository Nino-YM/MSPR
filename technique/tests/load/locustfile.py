"""
Tests de charge — API EDF Prediction
Locust : locust -f tests/load/locustfile.py --host=http://localhost:8000

Objectif SLA : 100 utilisateurs simultanés, temps de réponse P95 < 500ms, taux d'erreur < 1%
"""
import random
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner


# Token JWT pré-généré pour les tests de charge
# En production : utiliser le vrai endpoint /auth/token
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"  # Placeholder — générer avec create_access_token


def generate_prediction_payload():
    """Génère une requête de prédiction aléatoire réaliste."""
    month = random.randint(1, 12)
    is_winter = month in [11, 12, 1, 2, 3]
    base_temp = 5.0 if is_winter else 20.0
    temp_mean = base_temp + random.uniform(-3, 3)

    return {
        "date": f"2025-{month:02d}-{random.randint(1, 28):02d}",
        "temperature_moyenne": round(temp_mean, 1),
        "temperature_min": round(temp_mean - random.uniform(2, 5), 1),
        "temperature_max": round(temp_mean + random.uniform(2, 8), 1),
        "type_jour": random.choice([0, 0, 0, 0, 0, 1, 1, 2]),  # Surtout ouvrés
        "model": random.choice(["random_forest", "random_forest", "random_forest",
                                  "decision_tree", "rbf_network"])
    }


class PredictionUser(HttpUser):
    """Utilisateur simulé — opérateur EDF effectuant des prédictions."""
    wait_time = between(1, 3)  # Pause entre 1 et 3 secondes entre les requêtes

    def on_start(self):
        """Authentification au démarrage."""
        response = self.client.post(
            "/auth/token",
            params={"username": "operateur_edf", "password": "edf2025!"},
            name="/auth/token"
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {"Authorization": f"Bearer {TEST_TOKEN}"}

    @task(10)
    def predict_random_forest(self):
        """Prédiction avec Random Forest — cas le plus fréquent (80% du trafic)."""
        payload = generate_prediction_payload()
        payload["model"] = "random_forest"
        with self.client.post(
            "/predict",
            json=payload,
            headers=self.headers,
            name="/predict [random_forest]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "consommation_predite_mw" not in data:
                    response.failure("Réponse mal formée : champ manquant")
                elif data["consommation_predite_mw"] <= 0:
                    response.failure("Prédiction négative ou nulle")
                elif data["inference_time_ms"] > 500:
                    response.failure(f"Inférence trop lente : {data['inference_time_ms']}ms")
                else:
                    response.success()
            elif response.status_code == 503:
                response.failure("Modèle non disponible")
            else:
                response.failure(f"Erreur HTTP {response.status_code}")

    @task(3)
    def predict_other_model(self):
        """Prédiction avec un autre modèle (20% du trafic)."""
        payload = generate_prediction_payload()
        model = random.choice(["decision_tree", "rbf_network"])
        payload["model"] = model
        self.client.post(
            "/predict",
            json=payload,
            headers=self.headers,
            name=f"/predict [{model}]"
        )

    @task(5)
    def check_health(self):
        """Vérification de santé — monitoring externe simulé."""
        with self.client.get("/health", name="/health", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "unhealthy":
                    response.failure("API en état unhealthy")
                else:
                    response.success()

    @task(2)
    def list_models(self):
        """Liste des modèles disponibles."""
        self.client.get("/models", headers=self.headers, name="/models")

    @task(1)
    def get_metrics(self):
        """Métriques Prometheus."""
        self.client.get("/metrics", name="/metrics")


class AnalystUser(HttpUser):
    """Utilisateur simulé — analyste accédant aux métriques des modèles."""
    wait_time = between(5, 15)
    weight = 1  # Moins fréquent que les opérateurs

    def on_start(self):
        response = self.client.post(
            "/auth/token",
            params={"username": "analyste", "password": "analyse2025!"},
            name="/auth/token"
        )
        if response.status_code == 200:
            self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
        else:
            self.headers = {}

    @task(5)
    def get_model_metrics(self):
        model = random.choice(["random_forest", "decision_tree", "rbf_network", "knn"])
        self.client.get(
            f"/models/{model}/metrics",
            headers=self.headers,
            name="/models/{model}/metrics"
        )

    @task(3)
    def predict(self):
        payload = generate_prediction_payload()
        self.client.post("/predict", json=payload, headers=self.headers,
                          name="/predict [analyst]")


# ── Événements Locust ─────────────────────────────────────────────────────────

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "=" * 60)
    print("DÉBUT TEST DE CHARGE — API EDF Prediction")
    print("Objectifs SLA :")
    print("  - Temps réponse P95 < 500ms")
    print("  - Taux d'erreur < 1%")
    print("  - 100 utilisateurs simultanés")
    print("=" * 60 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    error_rate = (total_failures / total_requests * 100) if total_requests > 0 else 0
    p95 = stats.total.get_response_time_percentile(0.95)

    print("\n" + "=" * 60)
    print("RÉSULTATS TEST DE CHARGE")
    print("=" * 60)
    print(f"Requêtes totales : {total_requests:,}")
    print(f"Échecs          : {total_failures:,} ({error_rate:.2f}%)")
    print(f"P95 latence     : {p95:.0f}ms")

    sla_met = error_rate < 1.0 and (p95 or 0) < 500
    print(f"\nSLA : {'✅ RESPECTÉ' if sla_met else '❌ NON RESPECTÉ'}")
    print("=" * 60 + "\n")
