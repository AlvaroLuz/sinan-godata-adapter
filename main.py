import os
import importlib
import pandas as pd
import logging 

from core.adapters import GodataAuth, GodataApiClient
from core.sinan_processor import Processor, SinanDataProcessor
from core.add_sinan_case import AddSinanCaseService
from core.sinan_case_mapper import SinanCaseMapper
from core.logger import logger  
from dotenv import load_dotenv

load_dotenv()

logger. setLevel(logging.DEBUG)
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")


def run_pipeline(disease_name, repository):
    logger.info("Iniciando pipeline para a doença: %s", disease_name)
    disease_module = importlib.import_module(f"diseases.{disease_name}")
    logger.info("Módulo da doença carregado: %s", disease_module)

    lines_to_treat = None  # None para ler todas as linhas
    logger.info("Lendo dados do repositório: %s", repository)
    df = pd.read_excel(repository, nrows=lines_to_treat,dtype=str)
    logger.info("Dados lidos com sucesso: %s linhas", len(df))


    #processamento padrao dos dados
    standard_processor = SinanDataProcessor()
    df = standard_processor.run(df)

    #processamento especifico da doença
    logger.info("Iniciando processamento específico para a doença: %s", disease_name)
    processor = Processor.register(disease_module.DiseaseProcessor)
    disease_processor = processor()
    #df = disease_processor.run(df)
    logger.info("Processamento específico concluído.")

    #mapeamento dos dados
    mapper = SinanCaseMapper(questionnaire_mapping=disease_module.QUESTIONNAIRE_MAPPING)
    cases = mapper.run(df)
    
    

    #configurando cliente da API
    auth = GodataAuth(API_URL, API_TOKEN)
    token = auth.login(username=API_USERNAME, password=API_PASSWORD)
    api_client = GodataApiClient(base_url=API_URL, token=token, session=auth.session)
    
    service = AddSinanCaseService(api_client, disease_module.QUESTIONNAIRE_MAPPING)
    #service.run(cases)
    # try:
    #     reference_data = api_client.get_reference_data()
    #     #reference_data = json.dumps(reference_data, indent=2)
    #     reference_data = [ (item["value"] if "ADDRESS" in item["value"] else "") for item in reference_data]
    #     logger.info("Dados de referência obtidos: %s", reference_data)
    # except ConnectionError as e:
    #     logger.error("Erro ao obter dados de referência: %s", e)
    #     return


if __name__ == "__main__":
    run_pipeline("sarampo", "data/input/Sarampo.xlsx")