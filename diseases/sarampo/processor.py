import pandas as pd

class DiseaseProcessor:
    def __init__(self): 
        pass
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        # Implement disease-specific processing here
        # "outcomeId": "EVOLUCAO",
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