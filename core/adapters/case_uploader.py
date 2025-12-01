from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
from dataclasses import asdict
from typing import List
from pprint import pprint

from core.domain.models import GodataCase
from core.domain.ports import CasesOutputPort
from core.infra.client import GodataApiClient

from core.logger import logger

class CaseUploader(CasesOutputPort):
    def __init__(self, api_client: GodataApiClient, max_workers: int = 5):
        self.api_client = api_client
        self.max_workers = max_workers

    
    def _send_case(self, caso: GodataCase, case_id: str = None) -> dict:
        """Envia um caso individual para a API e retorna o resultado"""
        try:
            if case_id:
                response = self.api_client.put_case(caso.outbreakId, case_id, asdict(caso))
            else:
                response = self.api_client.post_case(caso.outbreakId, asdict(caso))

            logger.info("Caso NU_NOTIFIC=%s adicionado com sucesso.", caso.visualId)
            return {
                "NU_NOTIFIC": caso.visualId,
                "status": "success",
                "response_id": response.get("id"),
            }
        except Exception as e:
            logger.error("Erro ao adicionar caso NU_NOTIFIC=%s: %s", caso.visualId, e)
            return {
                "NU_NOTIFIC": caso.visualId,
                "status": "error",
                "error_message": str(e),
            }

    def send_cases(self,  casos: List[GodataCase], outbreak_id: str) -> List[dict]:
        """Executa envio de casos em paralelo"""
        results = []
        cases_repository = self.api_client.get_cases(outbreak_id)
        existing_cases = {case['visualId']: case['id'] for case in cases_repository}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_case = {
                executor.submit(
                    self._send_case, 
                    caso=caso, 
                    case_id=existing_cases.get(caso.visualId, None)
                ): caso for caso in casos
            }
            for future in as_completed(future_to_case):
                results.append(future.result())
        return results