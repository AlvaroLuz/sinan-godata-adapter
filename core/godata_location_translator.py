import pandas as pd
from .logger import logger

class GodataLocationTranslator:
    def __init__(self, api_client):
        self.api_client = api_client
        logger.info("Carregando localizações do Go.Data")
        self.locations = next((pais for pais in self.api_client.get_locations() if pais["location"].get("name") == "Brasil"), None)
        logger.info("Localizações carregadas com sucesso")
        for estado in self.locations["children"]:
            logger.debug("Verificando estado: %s", estado["location"].get("name"))

    def resolve_locations(self, uf: str, municipio: str):
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
    
    def run(self, cases: pd.DataFrame) -> dict:
        for index, row in cases.iterrows():
            logger.info("Resolvendo endereço para o caso: (%s/%s)", index + 1, len(cases))
            
            uf = row.get("UF RESIDÊNCIA", "")

            try:
                location_id = self.resolve_locations(
                    uf,
                    row.get("MUNICIPIO RESIDÊNCIA", "")
                )

                if location_id:
                    cases.at[index, "MUNICIPIO RESIDÊNCIA"] = location_id
                    logger.info("Endereço resolvido: %s", location_id)
                else:
                    logger.warning("Não foi possível resolver o endereço para o caso: %s", row["NU_NOTIFIC"])
                    raise Exception("Endereço não resolvido")
                
            except Exception as e:
                logger.error("Erro ao resolver endereço para o caso %s: %s", row["NU_NOTIFIC"], e)
                logger.debug("UF RESIDÊNCIA: %s, MUNICIPIO RESIDÊNCIA: %s", uf, row.get("MUNICIPIO RESIDÊNCIA", ""))
                   
        return cases