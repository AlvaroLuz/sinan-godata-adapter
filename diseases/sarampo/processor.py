import pandas as pd
from datetime import datetime, timezone, timedelta
import re
class DiseaseProcessor:
    def __init__(self): 
        pass

    def string_to_iso_utc(self, date_str: str) -> str:
        """
        Converte uma string de data para ISO 8601 UTC.
        Detecta automaticamente:
        - String no formato Excel (número serial)
        - String no formato ISO 8601
        
        Args:
            date_str (str): string representando a data
        
        Returns:
            str: data no formato 'YYYY-MM-DDTHH:MM:SS.mmmZ'
        """
        if pd.isna(date_str):
            return ""
        
        date_str = date_str.strip()
        
        if date_str == "" or date_str is None or date_str.lower() == "nan":
            return ""

        ISO_Z_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
        # Se já estiver em ISO Z, converte direto para datetime
        if ISO_Z_REGEX.match(date_str):
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        
        # Tenta converter como ISO 8601
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            # Se falhar, tenta converter como número Excel
            try:
                excel_number = float(date_str)
                excel_start = datetime(1899, 12, 30, tzinfo=timezone.utc)
                dt = excel_start + timedelta(days=excel_number)
            except ValueError:
                raise ValueError(f"Formato de data não reconhecido: {date_str}")
        
        # Garante que está em UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        
        return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        # Implement disease-specific processing here
        # "outcomeId": "EVOLUCAO",

        data_columns = ["DT_COL_1", "DT_COL_2", "DT_INICIO_", "DT_FEBRE"]
        for col in data_columns:
            if col in df.columns:
                df[col] = df[col].apply(self.string_to_iso_utc) 
                
        evolucao_map = {
            "1": "CURA",
            "2": "ÓBITO POR DOENÇA EXANTEMÁTICA",
            "3": "ÓBITO POR OUTRAS CAUSAS",
            "9": "",
            "": ""
        } 
        df["EVOLUCAO"] = df["EVOLUCAO"].map(evolucao_map).fillna("")
        # --- Criar coluna CLASSIFICACAO_FINAL ---
        # "CLASSIFICAÇÃO FINAL",
        classificacao_final_map = {"1": "SARAMPO", "2": "RUBEOLA", "3": "DISCARDED", "": ""}
        df["CLASSIFICACAO_FINAL"] = df["EVOLUCAO"].map(classificacao_final_map).fillna("")

        return df