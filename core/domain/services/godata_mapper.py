from typing import Any, Dict, List
from datetime import datetime, timezone

from core.adapters import (
    IBGELocationIdTranslator,
    GodataLocationTranslator,
    GodataOutbreakTranslator
) 

from core.adapters.translation.translation_registry import translation_registry

from core.domain.models import (
    GodataCase, 
    SinanCase, 
    Address, 
    Document, 
)

class GodataMapperService:
    def __init__(   self,                
                    godata_location_translator: GodataLocationTranslator, 
                    ibge_location_translator: IBGELocationIdTranslator,
                ):

        self.godata_location_translator = godata_location_translator
        self.ibge_location_translator = ibge_location_translator
    
    
    def _get_full_address(self, logrado, numero, complemento) -> str:
        parts = [logrado, numero, complemento]
        return ", ".join(part for part in parts if part)
    
    def _datetime_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return None
        
    def map(    
        self, 
        sinan_case: SinanCase, 
        questionnaire_answers: Dict[str, List[Dict[str, Any]]], 
        disease_name: str,
        outbreak_id: str       
    ) -> GodataCase:
        
        return GodataCase (
                visualId=f"{sinan_case.nu_notific}",
                firstName=sinan_case.nm_pacient,
                gender=translation_registry.translate("gender",sinan_case.cs_sexo),
                dob=self._datetime_serializer(sinan_case.dt_nasc),
                pregnancyStatus=translation_registry.translate("pregnancy_status", sinan_case.cs_gestant),
                documents=(                                 
                    [] if not sinan_case.id_cns_sus else [  
                        Document(                           
                            number= sinan_case.id_cns_sus, 
                            type= translation_registry.translate("document_type", "CNS")                      
                        )
                    ]
                ),
                addresses=[
                    Address(
                        typeId= translation_registry.translate("address_type", "Endereço Atual"),
                        addressLine1=   self._get_full_address(
                                            sinan_case.nm_logrado, 
                                            sinan_case.nu_numero, 
                                            sinan_case.nm_complemento
                                        ),
                        locationId=self.godata_location_translator.translate(
                            *self.ibge_location_translator.get_location(sinan_case.municipio_residencia)
                        ),
                        phoneNumber=sinan_case.nu_telefon,  
                        postalCode=sinan_case.nu_cep
                    )
                ], 
                usualPlaceOfResidenceLocationId=self.godata_location_translator.translate(
                    *self.ibge_location_translator.get_location(sinan_case.municipio_residencia)
                ),
                outbreakId=outbreak_id,
                outcomeId=translation_registry.translate(f"{disease_name}_outcome", sinan_case.evolucao),
                classification=translation_registry.translate(f"{disease_name}_case_classification", sinan_case.classificacao_final),
                dateOfReporting=self._datetime_serializer(sinan_case.dt_notific),
                dateOfOnset=self._datetime_serializer(sinan_case.dt_sin_pri),
                updatedAt=self._datetime_serializer(datetime.now(timezone.utc)),
                questionnaireAnswers=questionnaire_answers
            )
    

    




