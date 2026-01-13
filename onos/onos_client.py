import requests
from requests.auth import HTTPBasicAuth
class ONOSClient:
    def __init__(self, url, user, pwd):
        self.url = url
        self.auth = HTTPBasicAuth(user, pwd)
    def deploy_intent(self, intent):
        return requests.post(
            f"{self.url}/intents",
            json=intent,
            auth=self.auth
        )
