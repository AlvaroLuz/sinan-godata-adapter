import pandas as pd
from datetime import datetime
from typing import Dict, Any
from dataclasses import fields

from core.domain.models import IBGEId
from core.domain.diseases.disease_registry import disease_registry
from core.adapters import IBGELocationIdTranslator
from core.logger import logger
class DiseaseMapperService:
    def __init__(self, disease_name: str, ibge_location_translator: IBGELocationIdTranslator):
        try:
            disease_module = disease_registry.get(disease_name)
        except KeyError:
            raise ValueError(f"Disease '{disease_name}' is not registered.")
        
        self.questionnaire_cls = disease_module.questionnaire_cls           
        self.questionnaire_map = disease_module.questionnaire_map
        self.ibge_location_translator = ibge_location_translator

    def _resolve_date(self, date_str: Any) -> datetime:
        try:
            return [{"value": datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").isoformat()}]
        except Exception:
            return  [{}]
    
    def map(self, row: pd.Series) -> Dict[str, Dict[str, Any]]:
        answers = {}
        for field_info in fields(self.questionnaire_cls):
            column_name = self.questionnaire_map.get(field_info.name)
            
            if row.get(column_name, "") == "":
                answers[field_info.name] = [{}]
                continue
            
            if str(field_info.type) == "typing.Optional[datetime.datetime]":
                answers[field_info.name] = self._resolve_date(row.get(column_name))

            elif str(field_info.type) == "typing.Optional[core.domain.models.IBGEId]":
                answers[field_info.name] = [{
                    "value": self.ibge_location_translator.get_municipio(row.get(column_name))
                }]

            else:
                answers[field_info.name] = [{"value": row.get(column_name)}]

        return answers