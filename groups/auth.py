from pathlib import Path
from locust import HttpUser, constant ,events
from locust.exception import LocustError, StopUser

PWD = Path(__file__).parent.parent

auth_token = None
refresh_token = None



@events.request.add_listener
def refresh_auth_token(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    global auth_token
    if response.status_code == 401:
        auth_token = None
    if response.status_code > 500:
        raise StopUser()

class AuthenticatedUser(HttpUser):
    wait_time = constant(0.1)  # 1000 users will result in 100 requests per second
    abstract = True

    def login(self):
        global auth_token, refresh_token

        response = self.client.post(
                "/api/v1/auth/login/",
                {"username": "devdistrictadmin", "password": "Coronasafe@123"},
                timeout=30
            )
        
        response.raise_for_status()

        if response.status_code == 200:
            tokens = response.json()
            auth_token = tokens['access']
            refresh_token = tokens['refresh']
            self.client.headers = {"Authorization": f"Bearer {tokens['access']}"}
            with open(PWD / "refresh_token.txt", "w") as rt:
                rt.write(tokens['refresh'])
        else:
            print("login", response.status_code)
            raise LocustError()

    def refresh_auth_token(self, rt):
        global auth_token, refresh_token
        response = self.client.post(
            "/api/v1/auth/token/refresh/", json={"refresh": rt}, timeout=30
        )

        if response.status_code == 200:
            tokens = response.json()
            auth_token = tokens['access']
            self.client.headers = {"Authorization": f"Bearer {tokens['access']}"}

        elif response.status_code == 401:
            auth_token = None
            refresh_token = None
            self.login()
            print("refresh", response.status_code)

    def authenticate(self):
        global auth_token, refresh_token
        if auth_token:
            self.client.headers = {"Authorization": f"Bearer {auth_token}"}
        elif refresh_token:
            self.refresh_auth_token(refresh_token)
        else:
            try:
                with open(PWD / "refresh_token.txt") as f:
                    refresh_token = f.read().strip()
                self.refresh_auth_token(refresh_token)
            except FileNotFoundError:
                self.login()

    def on_start(self):
        self.authenticate()