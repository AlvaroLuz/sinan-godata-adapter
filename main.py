import os
import importlib
import pandas as pd
import logging 

from core.adapters import GodataAuth, GodataApiClient
from core.sinan_processor import Processor, SinanDataProcessor
from core.add_sinan_case import AddSinanCaseService
from core.sinan_case_mapper import SinanCaseMapper
from core.godata_location_translator import GodataLocationTranslator
from core.logger import logger  
from core.mappers import LocationIdMapper
from dotenv import load_dotenv

load_dotenv()

logger. setLevel(logging.DEBUG)
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")



def run_pipeline(disease_name, repository, lines_to_treat = None):

    logger.info("Lendo dados do repositório: %s", repository)
    
    df = pd.read_excel(repository, nrows=lines_to_treat,dtype=str)

    residence_mapper = LocationIdMapper("data/input/Dic_Mun_Res.xlsx")
    
    logger.info("Dados lidos com sucesso: %s linhas", len(df))
    
    
    logger.info("Iniciando processamento específico para a doença: %s", disease_name)
    
    disease_module = importlib.import_module(f"diseases.{disease_name}")
    
    logger.info("Módulo da doença carregado: %s", disease_module)
    #processamento especifico da doença
    processor = Processor.register(disease_module.DiseaseProcessor)
    disease_processor = processor()
    df = disease_processor.run(df)
    
    logger.info("Processamento específico concluído.")
    
    
    #processamento padrao dos dados
    standard_processor = SinanDataProcessor(residence_mapper=residence_mapper)
    df = standard_processor.run(df, anonymous_data=True)
    
    
    #configurando cliente da API
    auth = GodataAuth(API_URL, API_TOKEN)
    token = auth.login(username=API_USERNAME, password=API_PASSWORD)
    api_client = GodataApiClient(base_url=API_URL, token=token, session=auth.session)

    #resolver localizações
    location_solver = GodataLocationTranslator(api_client)
    location_solver.run(df)

    #mapeamento dos dados
    mapper = SinanCaseMapper(questionnaire_mapping=disease_module.QUESTIONNAIRE_MAPPING)
    cases = mapper.run(df)
    
    adapter= mapper.adapter
    with open("./data/output/cases_debug.json", "w") as f:
        for case in cases:
            f.write(adapter.dump_json(case, indent=2).decode())
            f.write(",\n")

    service = AddSinanCaseService(api_client, disease_module.QUESTIONNAIRE_MAPPING)
    #service.run(cases)


if __name__ == "__main__":
    run_pipeline("sarampo", "data/input/base_enxant.xlsx")