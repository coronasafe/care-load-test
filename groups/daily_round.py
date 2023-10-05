from groups.auth import AuthenticatedUser, task
import random
from datetime import datetime

payload = {
    "rounds_type": "NORMAL",
    "patient_category": "Stable",
    "taken_at": datetime.utcnow().isoformat(),
    "additional_symptoms": [2],
    "admitted_to": "Select",
    "physical_examination_info": "test",
    "other_details": "test",
    "consultation": "cd78c89f-6574-431e-bc7a-4f3d9561debe",
    "recommend_discharge": False,
    "action": "NO_ACTION",
    "review_interval": -1,
    "pulse": None,
    "resp": 14,
    "temperature": 98,
    "rhythm": 5,
    "rhythm_detail": None,
    "ventilator_spo2": 98,
}


class DailyRoundUser(AuthenticatedUser):
    consultation = "cd78c89f-6574-431e-bc7a-4f3d9561debe"

    @task(4)
    def get_daily_round_list(self):
        self.client.get(f"/api/v1/consultation/{self.consultation}/daily_rounds/")

    @task(3)
    def get_daily_round(self):
        daily_rounds_list = self.client.get(
            f"/api/v1/consultation/{self.consultation}/daily_rounds/"
        ).json()["results"]
        daily_round_id = random.randint(0, len(daily_rounds_list) - 1)
        with self.client.rename_request(
            f"/api/v1/consultation/{self.consultation}/daily_rounds/[id]"
        ):
            self.client.get(
                f"/api/v1/consultation/{self.consultation}/daily_rounds/{daily_rounds_list[daily_round_id]['id']}/"
            )

    @task(3)
    def post_daily_round(self):
        self.client.post(
            f"/api/v1/consultation/{self.consultation}/daily_rounds/", json=payload
        )
