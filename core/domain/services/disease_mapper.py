import pandas as pd
from datetime import datetime
from typing import Dict, Any
from core.domain.diseases.disease_registry import disease_registry
from dataclasses import fields
from core.domain.models import IBGEId

class DiseaseMapperService:
    def __init__(self, disease_name: str):
        try:
            disease_module = disease_registry.get(disease_name)
        except KeyError:
            raise ValueError(f"Disease '{disease_name}' is not registered.")
        
        self.questionnaire_cls = disease_module.questionnaire_cls           
        self.questionnaire_map = disease_module.questionnaire_map

    def map(self, row: pd.Series) -> Dict[str, Dict[str, Any]]:
        answers = {}
        for field_info in fields(self.questionnaire_cls):
            column_name = self.questionnaire_map.get(field_info.name)

            if field_info.type is datetime:
                answers[field_info.name] = [{"date": row.get(column_name)}]
            elif field_info.type is IBGEId:
                answers[field_info.name] = [{
                    "value": self.ibge_location_translator.get_municipio(row.get(column_name))
                }]
            else:
                answers[field_info.name] = [{"value": row.get(column_name)}]
        return answers