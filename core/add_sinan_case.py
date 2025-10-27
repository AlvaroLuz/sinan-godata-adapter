import pandas as pd

from pydantic import TypeAdapter
from typing import Dict, List, Any

from .adapters.api_client import GodataApiClient
from .sinan_processor import SinanDataProcessor
from .entities import SinanCase
from .logger import logger
from .sinan_case_mapper import SinanCaseMapper


class AddSinanCaseService: 
    def __init__(self, api_client: GodataApiClient, processor: SinanDataProcessor, questionnaire_mapping: dict): 
        self.api_client = api_client
        self.processor = processor
        self.questionnaire_mapping = questionnaire_mapping
        

    def run(self, df: pd.DataFrame, outbreak_name: str) -> pd.DataFrame:
        outbreak_id = self._get_outbreak_id(outbreak_name)
        self.mapper = SinanCaseMapper(outbreak_id, self.questionnaire_mapping)    
        self._add_sinan_case(df)

        return df

    def _add_sinan_case(self, df: pd.DataFrame) -> None:
        df = self.processor.run(df) 
        logger.info("Preprocessamento concluído")

        #mapeando os dados
        logger.info("Iniciando mapeamento dos dados para notificação")
        for i, row in df.iterrows():
            logger.info("Processando linha: (%s/%s)", i+1, len(df))            
            try:
                case = self.mapper._case_from_row(row)
                
                adapter = TypeAdapter(SinanCase)
                case_out = adapter.dump_json(case, indent=2).decode()
                logger.debug("Caso mapeado para notificação: %s", case.documents)
                
            except Exception as e:
                for column in df.columns:
                    if pd.notna(row[column]):
                        continue
                        #logger.debug("Coluna %s (%s): %s", column,type(row[column]), row[column])
                logger.error("Erro ao mapear caso %s: %s", i, e)
                continue
    
    def _get_outbreak_id(self, outbreak_name: str):
        outbreaks= self.api_client.get_outbreaks()
        outbreak_id = next((o["id"] for o in outbreaks if o["name"] == outbreak_name), None)

        if not outbreak_id:
            raise ValueError(f"Surto '{outbreak_name}' não encontrado.")
        
        logger.info("ID do surto obtido: %s", outbreak_id)
        return outbreak_id
