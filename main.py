import os
from dotenv import load_dotenv


from pprint import pprint

from core.infra.auth import GodataAuth
from core.infra.client import GodataApiClient
from core.adapters import (
    XlsxReader,
    GodataOutbreakTranslator,
    GodataLocationTranslator,
    IBGELocationIdTranslator,
    CaseUploader,
    CaseJsonWriter
)

from core.app.use_cases import (
    ImportSinanDataUseCase
)
from core.logger import logger

load_dotenv()
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")


if __name__ == "__main__":
    auth = GodataAuth(API_URL, API_TOKEN)
    token = auth.login(username=API_USERNAME, password=API_PASSWORD)
    api_client = GodataApiClient(base_url=API_URL, token=token, session=auth.session)

    xlsx_path = "data/input/base_enxant.xlsx"
    ibge_dictionary_path = "./data/input/Dic_Mun_Res.xlsx"
    
    
    use_case = ImportSinanDataUseCase(
        disease_module_name="sarampo",
        input_port=XlsxReader(file_path=xlsx_path),
        godata_outbreak_translator=GodataOutbreakTranslator(api_client=api_client),
        godata_location_translator=GodataLocationTranslator(api_client=api_client),
        ibge_location_translator=IBGELocationIdTranslator(dictionary_path=ibge_dictionary_path),
        #output_port=CaseJsonWriter(file_path="data/output/cases.json")
        output_port=CaseUploader(api_client=api_client)
    )

    use_case.execute("Sarampo",anonymize=True)
