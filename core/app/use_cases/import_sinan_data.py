from core.domain.ports import (
    CasesOutputPort, DataframeReader
)
from core.app.services import Preprocessor
from core.domain.services import (
    GoDataMapperService,
    DiseaseMapperService,
    SinanMapperService
)
from core.adapters import(
    GodataLocationTranslator,
    IBGELocationIdTranslator
)
from core.logger import logger



class ImportSinanDataUseCase:
    def __init__(
            self, 
            input_port: DataframeReader, 
            godata_location_translator: GodataLocationTranslator, 
            ibge_location_translator: IBGELocationIdTranslator,
            output_port: CasesOutputPort
        ):

        self.input_port = input_port
        self.sinan_mapper = SinanMapperService()
        self.disease_mapper = DiseaseMapperService()
        self.godata_mapper = GoDataMapperService(
            godata_location_translator=godata_location_translator,
            ibge_location_translator=ibge_location_translator
        ) 
        self.output_port = output_port

    def execute(self, disease_name: str, anonymize=False):
        df = self.input_port.read_dataframe()

        # Preprocessamento está na Application Layer (não no domínio)
        df = Preprocessor().run(df, anonymize)
        cases = []
        for _, row in df.iterrows():
            sinan_case = self.sinan_mapper.map(row)
            questionnaire_answers = self.disease_mapper.map(row)
            godata_case = self.godata_mapper.map(
                sinan_case=sinan_case, 
                questionnaire_answers=questionnaire_answers,
                disease=disease_name 
            )
           
            cases.append(godata_case)

        self.output_port.send_cases(cases)
        return cases