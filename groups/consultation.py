from groups.auth import AuthenticatedUser, task
import random


class ConsultationUser(AuthenticatedUser):
    @task
    def get_consultation_list(self):
        self.client.get("/api/v1/consultation/")

    @task
    def get_consultation(self):
        res = self.client.get("/api/v1/consultation/")
        data = res.json()
        consultation_id = random.randint(0, 10 - 1)
        with self.client.rename_request("/api/v1/consultation/[id]"):
            self.client.get(f"/api/v1/consultation/{res.json()['results'][consultation_id]['id']}/")
