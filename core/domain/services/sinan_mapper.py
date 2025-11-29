import pandas as pd
from datetime import datetime

from core.domain.models import SinanCase

class SinanMapperService:
    def __init__(self):
        pass

    def map(self, row: pd.Series) -> SinanCase:
        """mapeia uma linha do DataFrame para um objeto SinanCase."""
        return SinanCase(
            nu_notific= row.get("NU_NOTIFIC"),

            nm_pacient= row.get("NM_PACIENT"),
            dt_nasc = datetime.strptime(row.get("DT_NASC", ""), "%Y-%m-%d"),
            cs_sexo= row.get("CS_SEXO"),
            cs_gestant= row.get("CS_GESTANT"),
            id_cns_sus = row.get("ID_CNS_SUS", None),
            nu_telefon = row.get("NU_TELEFON"),

            nu_cep = row.get("NU_CEP", ""),
            municipio_residencia = row.get("MUNICIPIO RESIDÊNCIA"),
            
            evolucao = row.get("EVOLUCAO", ""),
            classificacao_final = row.get("CLASS_FIN", ""),
            dt_notific = datetime.strptime(row.get("DT_NOTIFIC", ""), "%Y-%m-%d") if row.get("DT_NOTIFIC", "") else None,
            
            nm_bairro = row.get("NM_BAIRRO", None),
            nm_logrado = row.get("NM_LOGRADO", None),
            nu_numero = row.get("NU_NUMERO", None),
            nm_complemento = row.get("NM_COMPLEM", None),
            
            dt_sin_pri = datetime.strptime(row.get("DT_SIN_PRI", ""), "%Y-%m-%d") if row.get("DT_SIN_PRI", "") else None,
        )
    
