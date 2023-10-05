from groups.auth import AuthenticatedUser, task
import random


class UserUser(AuthenticatedUser):
    @task(5)
    def get_current_user(self):
        self.client.get("/api/v1/users/getcurrentuser/")

    @task(3)
    def get_user_list(self):
        self.client.get("/api/v1/users/" )

    @task(1)
    def get_randon_user(self):
        users_list = self.client.get("/api/v1/users/").json()["results"]
        random_user = random.randint(0, len(users_list) - 1)
        with self.client.rename_request("/api/v1/users/[username]"):
            self.client.get(f"/api/v1/users/{users_list[random_user]['username']}/")
