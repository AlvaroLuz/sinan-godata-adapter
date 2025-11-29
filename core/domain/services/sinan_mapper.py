import pandas as pd
from datetime import datetime
from typing import Any

from core.domain.models import SinanCase
from core.logger import logger
from core.adapters.translation.translation_registry import translation_registry

class SinanMapperService:
    def __init__(self):
        pass
    def _resolve_date(self, date_str: Any) -> datetime:
        if isinstance(date_str, datetime):
            return date_str.date()   
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") if date_str else None
    
    def map(self, row: pd.Series) -> SinanCase:
        """mapeia uma linha do DataFrame para um objeto SinanCase."""
        return SinanCase(
            nu_notific= f'{row.get("NU_NOTIFIC", "")}',

            nm_pacient= row.get("NM_PACIENT"),
            dt_nasc = self._resolve_date(row.get("DT_NASC", "")),
            cs_sexo= f'{row.get("CS_SEXO", "")}',
            cs_gestant= f'{row.get("CS_GESTANT", "")}',
            id_cns_sus = row.get("ID_CNS_SUS", None),
            nu_telefon = row.get("NU_TELEFON"),

            nu_cep = row.get("NU_CEP", ""),
            municipio_residencia = f'{row.get("ID_MUNICIP", "")}',
            
            evolucao = f'{row.get("EVOLUCAO", "")}',
            classificacao_final = f'{row.get("CLASS_FIN", "")}',
            dt_notific = self._resolve_date(row.get("DT_NOTIFIC", "")),
            
            nm_bairro = f'{row.get("NM_BAIRRO", None)}',
            nm_logrado = f'{row.get("NM_LOGRADO", None)}',
            nu_numero = f'{row.get("NU_NUMERO", None)}',
            nm_complemento = f'{row.get("NM_COMPLEM", None)}',
            
            dt_sin_pri = self._resolve_date(row.get("DT_SIN_PRI", "")),
        )
    
