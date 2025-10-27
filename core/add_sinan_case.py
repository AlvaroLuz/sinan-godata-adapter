import json
import pandas as pd
from datetime import datetime
from pydantic import TypeAdapter
from typing import Dict, List, Any

from .adapters.api_client import GodataApiClient
from .sinan_processor import SinanDataProcessor
from .entities import SinanCase, Address, Document, Age
from .logger import logger

class AddSinanCaseService: 
    def __init__(self, api_client: GodataApiClient, processor: SinanDataProcessor, questionnaire_mapping: dict): 
        self.api_client = api_client
        self.processor = processor
        self.questionnaire_mapping = questionnaire_mapping
        self.outbreak_id = ""

    def _map_disease(self, df):
        pass

    def run(self, df: pd.DataFrame, outbreak_name: str) -> pd.DataFrame:
        self._get_outbreak_id(outbreak_name)
        self._map_default_case(df)
        self._map_disease(df)
        return df
    
    def _map_default_case(self, df: pd.DataFrame) -> pd.DataFrame:
        #preprocessando os dados
        logger.info("Iniciando preprocessamento dos dados")
        df = self.processor.run(df) 
        logger.info("Preprocessamento concluído")

        #mapeando os dados
        logger.info("Iniciando mapeamento dos dados para notificação")
        for i, row in df.iterrows():
            logger.info("Processando linha: (%s/%s)", i+1, len(df))            
            try:
                case = self._case_from_row(row)
                adapter = TypeAdapter(SinanCase)
                case_out = adapter.dump_json(case, indent=2).decode()
                logger.debug("Caso mapeado para notificação: %s", case_out)
                
            except Exception as e:
                for column in df.columns:
                    if pd.notna(row[column]):
                        logger.debug("Coluna %s (%s): %s", column,type(row[column]), row[column])
                logger.error("Erro ao mapear caso %s: %s", i, e)
                continue
    
    def _get_outbreak_id(self, outbreak_name: str):
        outbreaks= self.api_client.get_outbreaks()
        self.outbreak_id = next((o["id"] for o in outbreaks if o["name"] == outbreak_name), None)
        if not self.outbreak_id:
            raise ValueError(f"Surto '{outbreak_name}' não encontrado.")
        logger.info("ID do surto obtido: %s", self.outbreak_id)

    def _get_questionnaire_answers(self, row: pd.Series) -> Dict[str, List[Dict[str, Any]]]:
        answers = {}
        for key, value in self.questionnaire_mapping.items():
            answers[key] = [{"value": row.get(value)}]
        return answers


    def _case_from_row(self, row: pd.Series) -> SinanCase:
        return SinanCase(
            visualId=row.get("NU_NOTIFIC"),
            firstName=row.get("NM_PACIENT", "Lorem Ipsum"),
            gender=row.get("CS_SEXO"),
            pregnancyStatus=row.get("CS_GESTANT"),
        age=Age(
            years=int(row.get("IDADE"))
        )if row.get("IDADE") != "" else None,
        #dob=row.get("DT_NASC", None),
        outbreakId = self.outbreak_id,
        addresses=[
            Address(
                typeId=row.get("Endereço_Atual"),
                addressLine1=row.get("ENDEREÇO COMPLETO"),
                locationId=row.get("MUNICIPIO RESIDÊNCIA"),
                phoneNumber=row.get("NU_TELEFON") if pd.notna(row.get("NU_TELEFON")) else None,
                postalCode=row.get("NU_CEP"),
            )
        ],
        documents=[
            Document(
                number=row.get("ID_CNS_SUS"),
                type=row.get("TIPO DE DOCUMENTO")
            )
        ],
        outcomeId=row.get("EVOLUCAO"),
        classification=row.get("CLASSIFICAÇÃO FINAL"),
        dateOfReporting=row.get("DT_NOTIFIC"),
        dateOfOnset=row.get("DT_SIN_PRI"),
        updatedAt=row.get("Atualizado_em"),
        questionnaireAnswers=self._get_questionnaire_answers(row)
    )
