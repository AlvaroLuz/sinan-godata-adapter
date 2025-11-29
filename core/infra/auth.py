import requests
from typing import Optional

class GodataAuth:
    def __init__(self, base_url: str, api_token: Optional[str] = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token: Optional[str] = api_token

    def login(self, username: str, password: str) -> str:
        login_url = f"{self.base_url}/api/users/login?access_token={self.access_token}"
        response = self.session.post(login_url, data={"email": username, "password": password})

        if response.ok:
            self.access_token = response.json().get("id")
            if not self.access_token:
                raise ValueError("Token não retornado pelo login.")
            return self.access_token
        else:
            raise ConnectionError(f"Falha no login: {response.status_code}")