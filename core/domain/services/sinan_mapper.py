import pandas as pd
from datetime import datetime
from typing import Any

from core.domain.models import SinanCase
from core.logger import logger
from core.adapters.translation.translation_registry import translation_registry

class SinanMapperService:
    def _resolve_date(self, date_str: Any) -> datetime:
        if isinstance(date_str, datetime):
            return date_str.date()
        try:  
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") if date_str else None
        except Exception:
            return None
        
    def map(self, row: pd.Series) -> SinanCase:
        """mapeia uma linha do DataFrame para um objeto SinanCase."""
        return SinanCase(
            nu_notific= row.get("NU_NOTIFIC", ""),

            nm_pacient= row.get("NM_PACIENT"),
            dt_nasc = self._resolve_date(row.get("DT_NASC", "")),
            cs_sexo= row.get("CS_SEXO", ""),
            cs_gestant= row.get("CS_GESTANT", ""),
            id_cns_sus = row.get("ID_CNS_SUS", ""),
            nu_telefon = row.get("NU_TELEFON", ""),

            nu_cep = row.get("NU_CEP", ""),
            municipio_residencia = row.get("ID_MN_RESI", ""),
            
            evolucao = row.get("EVOLUCAO", ""),
            classificacao_final = row.get("CLASS_FIN", ""),
            dt_notific = self._resolve_date(row.get("DT_NOTIFIC", "")),
            
            nm_bairro = row.get("NM_BAIRRO", ""),
            nm_logrado = row.get("NM_LOGRADO", ""),
            nu_numero = row.get("NU_NUMERO", ""),
            nm_complemento = row.get("NM_COMPLEM", ""),
            
            dt_sin_pri = self._resolve_date(row.get("DT_SIN_PRI", "")),
        )
    
