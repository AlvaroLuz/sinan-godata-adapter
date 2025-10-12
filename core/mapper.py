import json
import pandas as pd
from datetime import datetime
from pydantic import TypeAdapter

from .adapters.api_client import GodataApiClient
from .base_processor import DefaultProcessor
from .entities import DefaultCase, Address, DocumentObject
from .logger import logger

class Mapper: 
    def __init__(self, api_client: GodataApiClient, processor: DefaultProcessor): 
        self.api_client = api_client
        self.processor = processor

    def run(self, df: pd.DataFrame, outbreak_name: str) -> pd.DataFrame:
        self._get_outbreak_id(outbreak_name)
        self._map_default_case(df)
        self._map_disease(df)
        return df
    def _get_outbreak_id(self, outbreak_name: str):
        outbreaks= self.api_client.get_outbreaks()
        self.outbreak_id = next((o["id"] for o in outbreaks if o["name"] == outbreak_name), None)
        if not self.outbreak_id:
            raise ValueError(f"Surto '{outbreak_name}' não encontrado.")
        logger.info("ID do surto obtido: %s", self.outbreak_id)
        

    def _create_default_case(self):
        default_case = DefaultCase(
            outbreakId=self.outbreak_id,
            firstName="",
            gender="",
            pregnancyStatus="",
            age=None,
            dob=None,
            documents=[],
            addresses=[],
            dateOfReporting=self.processor._insert_timestamp(),
            dateOfOnset=None,
            dateRanges=[],
            questionnaireAnswers={},
            outcomeId="",
            classification="",
            vaccinesReceived=[],
            wasContact=False,
            safeBurial=False,
            transferRefused=False,
            riskLevel="",
        )

        return default_case

    def _map_default_case(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.processor.run(df) 
        for _ , row in df.iterrows():
            new_case = self._create_default_case()
            
            new_case.firstName = row.get("NM_PACIENT", "Bananinha")
            new_case.gender = row.get("CS_SEXO", "")
            new_case.pregnancyStatus = row.get("CS_GESTANT", "LNG_REFERENCE_DATA_CATEGORY_PREGNANCY_STATUS_NONE")
            new_case.documents = [
                DocumentObject(
                    typeId=row.get("TIPO DE DOCUMENTO", ""), 
                    number=row.get("ID_CNS_SUS", "")
                )
            ] if row.get("TIPO DE DOCUMENTO", "")!="" else []
            new_case.addresses = [
                Address(
                    typeId=row.get("Endereço Atual", "LNG_REFERENCE_DATA_CATEGORY_ADDRESS_TYPE_USUAL_PLACE_OF_RESIDENCE"),
                    addressLine1=row.get("ENDEREÇO COMPLETO", ""),
                    locationId="a042112a-518e-4414-bcc1-5a187da0e47b",  # Placeholder, replace with actual mapping if available
                    geoLocationAccurate=False,
                    date=None,
                )   
            ]
            new_case.dateOfReporting = row.get("DT_NOTIFIC", self.processor._insert_timestamp())
            new_case.dateOfOnset = row.get("DT_SIN_PRI", None)
            if pd.notna(row.get("DT_NASC")):
                new_case.age = {"years":int(row["IDADE"])} if pd.notna(row.get("IDADE")) else {"years": 0 }
            else:
                new_case.dob = datetime.strptime(row["DT_NASC"], "%Y-%m-%dT%H:%M:%S.000Z")
            new_case.dob = row.get("DT_NASC", None)
            new_case.dateOfOnset = row.get("DT_SIN_PRI", None)

            self.api_client.get_cases(self.outbreak_id)
            adapter = TypeAdapter(DefaultCase)
            json_str = adapter.dump_json(new_case, indent=2).decode()
            print(json_str) 