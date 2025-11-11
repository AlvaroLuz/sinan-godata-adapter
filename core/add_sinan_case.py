from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import TypeAdapter
from .adapters.api_client import GodataApiClient
from .entities import SinanCase
from .logger import logger



class AddSinanCaseService:
    def __init__(self, api_client: GodataApiClient, questionnaire_mapping: dict, max_workers: int = 5):
        self.api_client = api_client
        self.questionnaire_mapping = questionnaire_mapping
        self.type_adapter = TypeAdapter(SinanCase)
        self.max_workers = max_workers

    def _serialize_case(self, caso: SinanCase) -> str:
        """Converte o caso em JSON usando Pydantic"""
        return self.type_adapter.dump_json(caso)

    def _send_case(self, caso: SinanCase) -> dict:
        """Envia um caso individual para a API e retorna o resultado"""
        try:
            case_json = self._serialize_case(caso)
            response = self.api_client.post_case(caso.outbreak_id, case_json)
            logger.info("Caso NU_NOTIFIC=%s adicionado com sucesso.", caso.NU_NOTIFIC)
            return {
                "NU_NOTIFIC": caso.NU_NOTIFIC,
                "status": "success",
                "response_id": response.get("id"),
            }
        except Exception as e:
            logger.error("Erro ao adicionar caso NU_NOTIFIC=%s: %s", caso.NU_NOTIFIC, e)
            return {
                "NU_NOTIFIC": caso.NU_NOTIFIC,
                "status": "error",
                "error_message": str(e),
            }

    def run(self, casos: List[SinanCase]) -> List[dict]:
        """Executa envio de casos em paralelo"""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_case = {executor.submit(self._send_case, caso): caso for caso in casos}
            for future in as_completed(future_to_case):
                results.append(future.result())
        return results