import pandas as pd
from datetime import datetime, timezone
from core.logger import logger

class Preprocessor:
    """
    Classe responsável pelo pré-processamento de DataFrames,
    incluindo normalização de valores ausentes e anonimização de dados sensíveis.
    """
    def __init__(self):
        pass
    def run(self, df: pd.DataFrame, anonymize_data: bool) -> pd.DataFrame:
            # 1. Normalizar valores ausentes
            mask = df.isin(["NA", "", None])
            df.where(~mask, "", inplace=True)
            df = df.fillna("")
            # 2. Anonimização (se solicitada)
            if anonymize_data:
                logger.info("Anonimizando dados sensíveis")

                initialize_cols = ["NM_PACIENT", "NU_CEP", "NU_TELEFON", "ID_CNS_SUS", "DT_NASC"]
                for col in initialize_cols:
                    if col not in df.columns:
                        df[col] = ""
                
                df["NM_PACIENT"] = "Paciente Anônimo"
                df["NU_CEP"] = "00000-000"
                df["NU_TELEFON"] = "(00)0000-0000"
                df["ID_CNS_SUS"] = "000000000000000"
                df["DT_NASC"] = datetime(2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            
            return df