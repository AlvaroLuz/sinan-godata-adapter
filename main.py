import os
from dotenv import load_dotenv



from core.infra.auth import GodataAuth
from core.infra.client import GodataApiClient
from core.adapters import (
    XlsxReader,
    GodataLocationTranslator,
    IBGELocationIdTranslator,
    CaseUploader
)

from core.app.use_cases import (
    ImportSinanDataUseCase
)

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
        input_port=XlsxReader(file_path=xlsx_path),
        godata_location_translator=GodataLocationTranslator(api_client=api_client),
        ibge_location_id_translator=IBGELocationIdTranslator(dictionary_path=ibge_dictionary_path),
        case_uploader=CaseUploader(api_client=api_client)
    )

    use_case.execute(disease_name="sarampo")
