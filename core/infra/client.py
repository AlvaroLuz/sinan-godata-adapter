from core.logger import logger
import requests
from typing import Any, Dict, Optional



class GodataApiError(Exception):
    """Exceção personalizada para erros da API Go.Data."""
    pass


class GodataApiClient:
    """Cliente HTTP para comunicação com a API Go.Data."""

    def __init__(self, base_url: str, token: str, session: Optional[requests.Session] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = session or requests.Session()

    # --- Métodos utilitários internos ---

    def _auth_params(self) -> Dict[str, str]:
        return {"access_token": self.token}

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Executa uma requisição HTTP genérica com tratamento de erros padrão."""
        url = f"{self.base_url}{endpoint}"
        params = kwargs.pop("params", {})
        params.update(self._auth_params())

        logger.debug(f"Requisição {method.upper()} → {url} com params={params} e kwargs={kwargs}")

        try:
            response = self.session.request(method, url, params=params, timeout=20, **kwargs)
            response.raise_for_status()
            logger.debug(f"Resposta {response.status_code}: {response.text[:200]}...")
            return response.json() if response.text else None
        except requests.RequestException as e:
            logger.error(f"Erro ao executar requisição {method.upper()} em {url}: {e}")
            raise GodataApiError(str(e)) from e

    # --- Métodos públicos da API ---

    def get_outbreaks(self) -> Any:
        return self._request("GET", "/api/outbreaks")

    def get_reference_data(self) -> Any:
        return self._request("GET", "/api/reference-data")

    def get_cases(self, outbreak_id: str) -> Any:
        return self._request("GET", f"/api/outbreaks/{outbreak_id}/cases")
    
    def get_locations(self, filter_params: Optional[Dict[str, str]] = None) -> Any:
        return self._request("GET", "/api/locations/hierarchical", params=filter_params or {})
    
    def post_case(self, outbreak_id: str, case_data: dict) -> Any:
        return self._request("POST", f"/api/outbreaks/{outbreak_id}/cases", json=case_data)

    def put_case(self, outbreak_id: str, case_id: str, case_data: dict) -> Any:
        return self._request("PUT", f"/api/outbreaks/{outbreak_id}/cases/{case_id}", json=case_data)