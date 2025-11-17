import pandas as pd
from .logger import logger

class GodataLocationTranslator:
    def __init__(self, api_client):
        self.api_client = api_client
        self.uf_map = {
            "AC": "Acre",
            "AL": "Alagoas",
            "AP": "Amapá",
            "AM": "Amazonas",
            "BA": "Bahia",
            "CE": "Ceará",
            "DF": "Distrito Federal",
            "ES": "Espírito Santo",
            "GO": "Goiás",
            "MA": "Maranhão",
            "MT": "Mato Grosso",
            "MS": "Mato Grosso do Sul",
            "MG": "Minas Gerais",
            "PA": "Pará",
            "PB": "Paraíba",
            "PR": "Paraná",
            "PE": "Pernambuco",
            "PI": "Piauí",
            "RJ": "Rio de Janeiro",
            "RN": "Rio Grande do Norte",
            "RS": "Rio Grande do Sul",
            "RO": "Rondônia",
            "RR": "Roraima",
            "SC": "Santa Catarina",
            "SP": "São Paulo",
            "SE": "Sergipe",
            "TO": "Tocantins",
        }
        logger.info("Carregando localizações do Go.Data")
        self.locations = next((pais for pais in self.api_client.get_locations() if pais["location"].get("name") == "Brasil"), None)
        logger.info("Localizações carregadas com sucesso")

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
            uf = row.get("UF NOTIFICAÇÃO", "")
            try:
                location_id = self.resolve_locations(
                    self.uf_map.get(uf, uf),
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
                logger.debug("UF NOTIFICAÇÃO: %s, MUNICIPIO RESIDÊNCIA: %s", self.uf_map.get(uf, uf), row.get("MUNICIPIO RESIDÊNCIA", ""))
                break
            
        return cases