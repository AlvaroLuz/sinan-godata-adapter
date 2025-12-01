from core.infra import GodataApiClient
from pprint import pprint
class GodataOutbreakTranslator: 
    def __init__(self, api_client: GodataApiClient):
        self.outbreaks = api_client.get_outbreaks()


    def translate(self, outbreak_name: str) -> str:
        outbreak_id = next((ob['id'] for ob in self.outbreaks if ob['name']== outbreak_name), None)

        if outbreak_id == None:
            raise ValueError(f"Agravo de nome '{outbreak_name}' não encontrado no GoData.") 
        
        return outbreak_id