from core.domain.ports import (
    CasesOutputPort, DataframeReader
)
from core.domain.services import (
    GodataMapperService,
    DiseaseMapperService,
    SinanMapperService
)
from core.app.services import Preprocessor

from core.adapters import(
    GodataLocationTranslator,
    IBGELocationIdTranslator,
    GodataOutbreakTranslator
)
from core.logger import logger



class ImportSinanDataUseCase:
    def __init__(
            self, 
            disease_module_name: str,
            input_port: DataframeReader, 
            godata_outbreak_translator: GodataOutbreakTranslator,
            godata_location_translator: GodataLocationTranslator, 
            ibge_location_translator: IBGELocationIdTranslator,
            output_port: CasesOutputPort
        ):
        
        self.disease_module_name = disease_module_name
        self.input_port = input_port
        self.sinan_mapper = SinanMapperService()

        self.disease_mapper = DiseaseMapperService(
            disease_name=disease_module_name, 
            ibge_location_translator=ibge_location_translator
        )
        self.godata_outbreak_translator = godata_outbreak_translator

        self.godata_mapper = GodataMapperService(
            godata_location_translator=godata_location_translator,
            ibge_location_translator=ibge_location_translator,
        ) 
        self.output_port = output_port

    def execute(self, godata_outbreak_name, anonymize=False):
        df = self.input_port.read_dataframe()

        # Preprocessamento está na Application Layer (não no domínio)
        df = Preprocessor().run(df, anonymize)

        outbreak_id = self.godata_outbreak_translator.translate(godata_outbreak_name)

        cases = []

        for index, row in df.iterrows():
            logger.info("Processando Dados (%s/%s)", index + 1, len(df))
            sinan_case = self.sinan_mapper.map(row)
            questionnaire_answers = self.disease_mapper.map(row)
            godata_case = self.godata_mapper.map(
                sinan_case = sinan_case, 
                questionnaire_answers = questionnaire_answers,
                disease_name = self.disease_module_name,
                outbreak_id = outbreak_id
            )
           
            cases.append(godata_case)
        logger.info("Casos mapeados, enviando...")
        self.output_port.send_cases(cases, outbreak_id)
        return cases