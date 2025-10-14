import os
import importlib
import pandas as pd
import logging 

from core.adapters import GodataAuth, GodataApiClient
from core.base_processor import BaseProcessor, DefaultProcessor
from core.mapper import Mapper
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

    processor = BaseProcessor.register(disease_module.DiseaseProcessor)
    base_processor = DefaultProcessor(processor())

    auth = GodataAuth(API_URL, API_TOKEN)
    token = auth.login(username=API_USERNAME, password=API_PASSWORD)
    api_client = GodataApiClient(base_url=API_URL, token=token, session=auth.session)
    
    
    mapper = Mapper(api_client, base_processor, disease_module.QUESTIONNAIRE_MAPPING)
    df_mapped = mapper.run(df, outbreak_name="Sarampo")
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