import requests
from requests.auth import HTTPBasicAuth

class ONOSClient:
    def __init__(self, url: str, user: str, pwd: str):
        self.url = url.rstrip("/")
        self.auth = HTTPBasicAuth(user, pwd)

    def post_intent(self, intent: dict):
        return requests.post(
            f"{self.url}/intents",
            json=intent,
            auth=self.auth,
            timeout=10
        )
