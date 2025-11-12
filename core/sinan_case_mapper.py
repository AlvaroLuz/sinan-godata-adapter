from typing import Any, Optional, Dict, List
from pydantic import TypeAdapter
import pandas as pd

from .entities import SinanCase, Address, Document, Age
from .logger import logger

class SinanCaseMapper:
    _DEFAULTS: dict[str, Any] = {
        "NM_PACIENT": "",
        "CS_SEXO": "",
        "CS_GESTANT": "",
        "IDADE": None,
        "NU_TELEFON": None,
        "ID_CNS_SUS": "",
        "TIPO DE DOCUMENTO": "",
        "EVOLUCAO": "",
        "CLASSIFICAÇÃO FINAL": "",
        "DT_NOTIFIC": None,
        "DT_SIN_PRI": None,
        "Atualizado_em": None,
        "NU_CEP": "",
        "ENDEREÇO COMPLETO": "",
        "MUNICIPIO RESIDÊNCIA": "",
        "Endereço_Atual": "",
        "NU_NOTIFIC": "",
    }

    def __init__(self, questionnaire_mapping: Optional[dict] = None):
        self.questionnaire_mapping = questionnaire_mapping or {}
        self.adapter = TypeAdapter(SinanCase)

    def run(self, df: pd.DataFrame) -> List[SinanCase]:
        logger.info("Iniciando mapeamento dos dados para notificação")
        cases = []

        for i, row in df.iterrows():
            logger.info("Processando linha: (%s/%s)", i + 1, len(df))
            try:
                case = self._case_from_row(row)
                #logger.debug("Caso mapeado para notificação: %s", case_out)
                cases.append(case)
            except Exception as e:
                logger.error("Erro ao mapear linha (%s/%s): %s", i + 1, len(df), e)

        logger.info("Mapeamento concluído: %s casos mapeados.", len(cases))
        return cases

    def _get_field_value(self, row: pd.Series, field: str) -> Optional[Any]:
        val = row.get(field, self._DEFAULTS.get(field))
        return val if pd.notna(val) and val != "" else self._DEFAULTS.get(field)

    def _case_from_row(self, row: pd.Series) -> SinanCase:
        return SinanCase(
            visualId=self._get_field_value(row, "NU_NOTIFIC"),
            firstName=self._get_field_value(row, "NM_PACIENT"),
            gender=self._get_field_value(row, "CS_SEXO"),
            pregnancyStatus=self._get_field_value(row, "CS_GESTANT"),
            age=Age(years=int(self._get_field_value(row, "IDADE"))) if self._get_field_value(row, "IDADE") not in (None, "", "NaN") else None,
            addresses=self._build_address(row),
            documents=self._build_document(row),
            outcomeId=self._get_field_value(row, "EVOLUCAO"),
            classification=self._get_field_value(row, "CLASSIFICAÇÃO FINAL"),
            dateOfReporting=self._get_field_value(row, "DT_NOTIFIC"),
            dateOfOnset=self._get_field_value(row, "DT_SIN_PRI"),
            updatedAt=self._get_field_value(row, "Atualizado_em"),
            questionnaireAnswers=self._get_questionnaire_answers(row),
        )

    def _build_address(self, row: pd.Series) -> List[Address]:
        return [Address(
            typeId=self._get_field_value(row, "Endereço_Atual"),
            addressLine1=self._get_field_value(row, "ENDEREÇO COMPLETO"),
            locationId=self._get_field_value(row, "MUNICIPIO RESIDÊNCIA"),
            phoneNumber=self._get_field_value(row, "NU_TELEFON"),
            postalCode=self._get_field_value(row, "NU_CEP"),
        )]

    def _build_document(self, row: pd.Series) -> List[Document]:
        id_sus = self._get_field_value(row, "ID_CNS_SUS")
        if not id_sus:
            return []
        return [
            Document(
                number=id_sus,
                type=self._get_field_value(row, "TIPO DE DOCUMENTO"),
            )
        ]

    def _get_questionnaire_answers(self, row: pd.Series) -> Dict[str, List[Dict[str, Any]]]:
        answers = {}
        for key, value in self.questionnaire_mapping.items():
            answers[key] = [{"value": row.get(value)}]
        return answers
