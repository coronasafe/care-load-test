from groups.auth import AuthenticatedUser, task
import random


class PatientUser(AuthenticatedUser):
    @task
    def get_patient_list(self):
        self.client.get("/api/v1/patient/")

    @task
    def get_patient(self):
        res = self.client.get("/api/v1/patient/")
        patient_id = random.randint(0, len(res.json()["results"]) - 1)
        with self.client.rename_request("/api/v1/patient/[id]"):
            self.client.get(f"/api/v1/patient/{res.json()['results'][patient_id]['id']}/")
