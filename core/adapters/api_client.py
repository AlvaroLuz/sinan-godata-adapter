import requests
from typing import Optional

class GodataApiClient:
    def __init__(self, base_url: str, token: str, session: Optional[requests.Session] = None):
        self.base_url = base_url
        self.access_token = token
        self.session = session or requests.Session()

    def _auth_params(self):
        return {"access_token": self.access_token}

    def get_outbreaks(self):
        url = f"{self.base_url}/api/outbreaks"
        response = self.session.get(url, params=self._auth_params())
        if response.ok:
            return response.json()
        raise ConnectionError(f"Erro ao buscar surtos: {response.status_code}")

    def get_reference_data(self):
        url = f"{self.base_url}/api/reference-data"
        response = self.session.get(url, params=self._auth_params())
        if response.ok:
            return response.json()
        raise ConnectionError(f"Erro ao buscar dados de referência: {response.status_code}")

    def get_cases(self, outbreak_id: str):
        url = f"{self.base_url}/api/outbreaks/{outbreak_id}/cases"
        response = self.session.get(url, params=self._auth_params())
        if response.ok:
            return response.json()
        raise ConnectionError(f"Erro ao buscar casos: {response.status_code}")

    def post_case(self, outbreak_id: str, case_data: dict):
        url = f"{self.base_url}/api/outbreaks/{outbreak_id}/cases"
        response = self.session.post(url, json=case_data, params=self._auth_params())
        if response.ok:
            return response.json()
        raise ConnectionError(f"Falha ao adicionar caso: {response.status_code}")

