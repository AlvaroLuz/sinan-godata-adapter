import pandas as pd

from pydantic import TypeAdapter
from typing import List


from .adapters.api_client import GodataApiClient
from .entities import SinanCase
from .logger import logger


class AddSinanCaseService: 
    def __init__(self, api_client: GodataApiClient, questionnaire_mapping: dict): 
        self.api_client = api_client
        self.questionnaire_mapping = questionnaire_mapping
        

    def run(self, casos: List[SinanCase]):
        return
        results = []
        for caso in casos:
            try:
                case_data = TypeAdapter(SinanCase).dump_json(caso)
                response = self.api_client.post_case(caso.outbreak_id, case_data)
                results.append({
                    "NU_NOTIFIC": caso.NU_NOTIFIC,
                    "status": "success",
                    "response_id": response.get("id"),
                })
                logger.info("Caso NU_NOTIFIC=%s adicionado com sucesso.", caso.NU_NOTIFIC)
            except Exception as e:
                results.append({
                    "NU_NOTIFIC": caso.NU_NOTIFIC,
                    "status": "error",
                    "error_message": str(e),
                })
                logger.error("Erro ao adicionar caso NU_NOTIFIC=%s: %s", caso.NU_NOTIFIC, e)
        
        return pd.DataFrame(results)

