from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime
from .logger import logger
from .utils import string_to_iso_utc
from .translation.registry import TranslationRegistry

class BaseProcessor(ABC):
    @abstractmethod
    def run(self, df: pd.DataFrame) -> pd.DataFrame :
        pass

class DefaultProcessor(BaseProcessor):
    def __init__(self, disease_processor: BaseProcessor):
        self.disease_processor = disease_processor
    
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._standard_treatment(df)
        df = self.disease_processor.run(df)
        return df

    def _treat_gender(self, value : str):
        mapping = TranslationRegistry.get("gender")
        return mapping.get(value, "")

    def _treat_pregnancy(self, value: str):
        mapping = TranslationRegistry.get("pregnancy_status")
        return mapping.get(value, "LNG_REFERENCE_DATA_CATEGORY_PREGNANCY_STATUS_NONE")
    
    def _treat_document(self, value : str):
        mapping = TranslationRegistry.get("document_type")
        return mapping.get("CNS") if pd.notna(value) and str(value).strip() != "" else ""

    def _get_current_address_type(self):
        mapping = TranslationRegistry.get("address_type")
        return mapping.get("Endereço Atual")

    def _insert_timestamp(self):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def _standard_treatment(self, df: pd.DataFrame) -> pd.DataFrame:
        # Implement standard data processing steps here
        logger.info("Iniciando tratamento padrão dos dados")
    
        #------ não precisa de tratamento ------------  ----
        # (dados pessoais)- talvez garantir que não fique nulo
        # "NM_PACIENT", "NU_CEP", "NU_TELEFON","ID_CNS_SUS" 
        # ------------------------------------------------
        
        # não precisa de tratamento? adicionar prefixo do caso, se precisar
        # "NU_NOTIFIC",

        # --- flags do godata ---
        # "Endereço_Atual" 
        df["Endereço Atual"] = self._get_current_address_type()
        # "CS_SEXO"
        df["CS_SEXO"] = df["CS_SEXO"].apply(self._treat_gender)
        # "CS_GESTANT"
        df["CS_GESTANT"] = df["CS_GESTANT"].apply(self._treat_pregnancy)
        # "TIPO DE DOCUMENTO"
        df["TIPO DE DOCUMENTO"] = df["ID_CNS_SUS"].apply(self._treat_document)
        # -----------------------

        # --- TIMESTAMPS --- 
        # "Atualizado_em"
        df["Atualizado_em"] = self._insert_timestamp()
        
        # "DT_NASC"
        if "DT_NASC" not in df.columns:
            df["DT_NASC"] = None
        else:
            df["DT_NASC"] = pd.to_datetime(df["DT_NASC"], errors="coerce").strftime("%Y-%m-%dT%H:%M:%S.000Z")
            # "IDADE"
            hoje = datetime.today()
            df["IDADE"] = (
                (hoje - df["DT_NASC"]).dt.days / 365.25
            ).round().astype("Int64")
        
        # "DT_SIN_PRI","DT_NOTIFIC" 
        df["DT_SIN_PRI"] = df["DT_SIN_PRI"].apply(string_to_iso_utc)
        df["DT_NOTIFIC"] = df["DT_NOTIFIC"].apply(string_to_iso_utc)
        #---------------------

        
        # --- Criação do Endereço Completo ---
        # "MUNICIPIO RESIDÊNCIA"
        # "ENDEREÇO COMPLETO"
        df["ENDEREÇO COMPLETO"] = (
            df[["NM_BAIRRO", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM"]]
            .fillna("")
            .agg(", ".join, axis=1)
            .str.strip(", ")
        )
        # ---------------------
    
        print(df)
        logger.info("Tratamento padrão dos dados concluído")
        #df = df.fillna("")

        # # --- Arrumar Municipio de Residencia ---
        # dic_mun_res = pd.read_excel("Dic_Mun_Res.xlsx")
        # tabela_merge = pd.merge(df, dic_mun_res, on="ID_MN_RESI", how="left")

        # # --- Arrumar Municipio de Notificação ---
        # dic_mun_not = pd.read_excel("Dic_Mun_NOT.xlsx")
        # tabela_merge2 = pd.merge(tabela_merge, dic_mun_not, on="ID_MUNICIP", how="left")

        # --- Substituir NAs por string vazia ---
        #tabela_merge2 = tabela_merge2.fillna("")

        #tabela_merge2.to_csv(caminho_arquivo, index=False)

        return df