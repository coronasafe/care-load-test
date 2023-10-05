from locust import HttpUser, task, constant

class HealthUser(HttpUser):
    wait_time = constant(1)

    @task
    def health_check(self):
        self.client.get("/health/")
