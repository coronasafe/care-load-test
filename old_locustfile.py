import os
import pickle
from pathlib import Path

from locust import HttpUser, constant, task

PWD = Path(__file__)


class AuthenticatedUser(HttpUser):
    wait_time = constant(0.1)  # 1000 users will result in 100 requests per second
    abstract = True

    def on_start(self):
        self.authenticate()

    def authenticate(self):
        try:
            with open(PWD / "token.pickle", "rb") as f:
                self.tokens = pickle.load(f)

        except FileNotFoundError:
            response = self.client.post(
                "/api/v1/auth/login/",
                {"username": "devdistrictadmin", "password": "Coronasafe@123"},
            )

            if response.status_code == 200:
                self.tokens = response.json()
                with open(PWD / "token.pickle", "wb") as f:
                    pickle.dump(self.tokens, f)

    def refresh_auth_token(self):
        response = self.client.post(
            "/api/v1/auth/token/refresh/", json={"refresh": self.tokens["refresh"]}
        )

        if response.status_code == 200:
            self.tokens = response.json()
            self.client.headers = {"Authorization": f"Bearer {self.tokens['access']}"}
        elif response.status_code == 401:
            os.remove("token.pickle")


# class HealthCheck(HttpUser):
#     wait_time = between(1, 5)

#     @task
#     def health_check(self):
#         self.client.get("/health/")


class UserCheck(AuthenticatedUser):
    wait_time = 0

    @task
    def get_current_user(self):
        self.client.get("/api/v1/users/getcurrentuser/")

    @task
    def get_user_list(self):
        self.client.get("/api/v1/users/")

    @task
    def get_facility_list(self):
        self.client.get("/api/v1/facility/")

    @task
    def get_facility(self):
        res = self.client.get("/api/v1/facility/")
        id = res.json()["results"][0]["id"]
        self.client.get(f"/api/v1/facility/{id}/")

    @task
    def get_patient_list(self):
        self.client.get("/api/v1/patient/")

    @task
    def get_patient(self):
        res = self.client.get("/api/v1/patient/")
        id = res.json()["results"][0]["id"]
        self.client.get(f"/api/v1/patient/{id}/")

    @task
    def get_consultation_list(self):
        self.client.get("/api/v1/consultation/")

    @task
    def get_consultation(self):
        res = self.client.get("/api/v1/consultation/")
        id = res.json()["results"][0]["id"]
        self.client.get(f"/api/v1/consultation/{id}/")

    @task
    def get_asset_bed_list(self):
        self.client.get("/api/v1/assetbed/")
