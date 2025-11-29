import pandas as pd
from core.logger import logger

class PreprocessDataframeUseCase:
    """
    Classe responsável pelo pré-processamento de DataFrames,
    incluindo normalização de valores ausentes e anonimização de dados sensíveis.
    """
    def __init__(self):
        pass
    def run(self, df: pd.DataFrame, anonymize_data: bool) -> pd.DataFrame:
            # 1. Normalizar valores ausentes
            mask = df.isin(["NA", "", None, pd.NA])
            df.where(~mask, "", inplace=True)
            
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
                df["DT_NASC"] = "2000-01-01"
            
            return df