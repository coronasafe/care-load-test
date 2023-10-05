from groups.auth import AuthenticatedUser, task
import random


class FacilityUser(AuthenticatedUser):
    @task
    def get_facility_list(self):
        self.client.get("/api/v1/facility/")

    @task
    def get_facility(self):
        res = self.client.get("/api/v1/facility/")
        facility_id = random.randint(0, len(res.json()["results"]) - 1)
        with self.client.rename_request("/api/v1/facility/[id]"):
            self.client.get(f"/api/v1/facility/{res.json()['results'][facility_id]['id']}/")
