import pandas as pd
from core.logger import logger

class GodataLocationTranslator:
    def __init__(self, api_client):
        self.api_client = api_client
        
        logger.info("Carregando localizações do Go.Data")
        
        self.locations = next((pais for pais in self.api_client.get_locations() if pais["location"].get("name") == "Brasil"), None)
        
        logger.info("Localizações carregadas com sucesso")
        

    def translate(self, municipio: str,  uf: str):
        uf_loc = next((estado for estado in self.locations["children"] if estado["location"].get("name") == uf), None)
        
        if not uf_loc:
            logger.warning("UF não encontrada: %s", uf)
            return
        
        if uf in ["Santa Catarina"]:
            for regiao in uf_loc["children"]:
                logger.debug("Verificando municípios: %s", regiao["location"].get("name"))
                municipio_loc = next((mun for mun in regiao["children"] if mun["location"].get("name") == municipio), None)
                if municipio_loc:
                    break
        else:
            municipio_loc = next((mun for mun in uf_loc["children"] if mun["location"].get("name") == municipio), None)

        if not municipio_loc:
            logger.warning("Município não encontrado: %s", municipio)
            return

        return municipio_loc["location"].get("id")
    

