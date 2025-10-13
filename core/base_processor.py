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
    
    # =====================================================
    # === MÉTODO PRINCIPAL ================================
    # =====================================================

    def _normalize_disease_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._apply_standard_treatment(df)
        logger.info("Iniciando processamento específico da doença")
        df = self.disease_processor.run(df)
        df = self._normalize_disease_data(df)
        logger.info("Processamento específico da doença concluído")
        return df
    
    # =====================================================
    # === TRATAMENTO PADRÃO ===============================
    # =====================================================
    def _apply_standard_treatment(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Iniciando tratamento padrão dos dados")

        df = df.copy()
        
        #setting godata flags as data
        self._normalize_address_flag(df)
        self._normalize_gender(df)
        self._normalize_pregnancy(df)
        self._normalize_document_type(df)
        
        #processing information
        self._process_birth_date(df)
        self._process_notification_dates(df)
        self._build_full_address(df)
        
        #inserting timestamp
        self._insert_timestamp(df)

        logger.info("Tratamento padrão dos dados concluído")
        return df

    # =====================================================
    # === MÉTODOS AUXILIARES ==============================
    # =====================================================
    #funcoes de normalizacao usando mapping para as flags do sistema do godata
    def _normalize_address_flag(self, df: pd.DataFrame) -> None:
        #alterar se for necessario novos tipos de endereco
        df["Endereço_Atual"] = self._map_address_type("Endereço Atual")

    def _normalize_gender(self, df: pd.DataFrame) -> None:
        if "CS_SEXO" in df.columns:
            df["CS_SEXO"] = df["CS_SEXO"].apply(self._map_gender)

    def _normalize_pregnancy(self, df: pd.DataFrame) -> None:
        if "CS_GESTANT" in df.columns:
            df["CS_GESTANT"] = df["CS_GESTANT"].apply(self._map_pregnancy_status)

    def _normalize_document_type(self, df: pd.DataFrame) -> None:
        if "ID_CNS_SUS" in df.columns:
            df["TIPO DE DOCUMENTO"] = df["ID_CNS_SUS"].apply(self._map_document_type)

    #funcoes que processam os dados
    def _process_birth_date(self, df: pd.DataFrame) -> None:
        if "DT_NASC" not in df.columns:
            df["DT_NASC"] = None
            #descomentar essa linha quando estiver usando dados não anonimizados
            #df["IDADE"] = None
            return

        df["DT_NASC"] = pd.to_datetime(df["DT_NASC"], errors="coerce")
        df["IDADE"] = self._calculate_age(df["DT_NASC"])
        df["DT_NASC"] = df["DT_NASC"].dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def _process_notification_dates(self, df: pd.DataFrame) -> None:
        for col in ("DT_SIN_PRI", "DT_NOTIFIC"):
            if col in df.columns:
                df[col] = df[col].apply(string_to_iso_utc)

    def _build_full_address(self, df: pd.DataFrame) -> None:
        required_cols = ["NM_BAIRRO", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        df["ENDEREÇO COMPLETO"] = (
            df[required_cols]
            .fillna("")
            .agg(", ".join, axis=1)
            .str.strip(", ")
        )

    def _calculate_age(self, birth_dates: pd.Series) -> pd.Series:
        today = pd.Timestamp.today()
        return ((today - birth_dates).dt.days / 365.25).round().astype("Int64")
    
    #timestamp simples
    def _insert_timestamp(self, df: pd.DataFrame) -> None:
        df["Atualizado_em"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # =====================================================
    # === FUNÇÕES DE MAPEAMENTO (PADRÃO: _map_<campo>) ===
    # =====================================================
    def _map_gender(self, value: str) -> str:
        mapping = TranslationRegistry.get("gender")
        return mapping.get(value, "")

    def _map_pregnancy_status(self, value: str) -> str:
        mapping = TranslationRegistry.get("pregnancy_status")
        return mapping.get(
            value, "LNG_REFERENCE_DATA_CATEGORY_PREGNANCY_STATUS_NONE"
        )

    def _map_document_type(self, value: str) -> str:
        mapping = TranslationRegistry.get("document_type")
        return (
            mapping.get("CNS")
            if pd.notna(value) and str(value).strip() != ""
            else ""
        )

    def _map_address_type(self, value: str) -> str:
        mapping = TranslationRegistry.get("address_type")
        return mapping.get(value, "")

    
    # def _standard_treatment(self, df: pd.DataFrame) -> pd.DataFrame:
    #     # Implement standard data processing steps here
    #     logger.info("Iniciando tratamento padrão dos dados")
    
    #     #------ não precisa de tratamento ------------  ----
    #     # (dados pessoais)- talvez garantir que não fique nulo
    #     # "NM_PACIENT", "NU_CEP", "NU_TELEFON","ID_CNS_SUS" 
    #     # ------------------------------------------------
        
    #     # não precisa de tratamento? adicionar prefixo do caso, se precisar
    #     # "NU_NOTIFIC",

    #     # --- flags do godata ---
    #     # "Endereço_Atual" 
    #     df["Endereço Atual"] = self._get_current_address_type()
    #     # "CS_SEXO"
    #     df["CS_SEXO"] = df["CS_SEXO"].apply(self._treat_gender)
    #     # "CS_GESTANT"
    #     df["CS_GESTANT"] = df["CS_GESTANT"].apply(self._treat_pregnancy)
    #     # "TIPO DE DOCUMENTO"
    #     df["TIPO DE DOCUMENTO"] = df["ID_CNS_SUS"].apply(self._treat_document)
    #     # -----------------------

    #     # --- TIMESTAMPS --- 
    #     # "Atualizado_em"
    #     df["Atualizado_em"] = self._insert_timestamp()
        
    #     # "DT_NASC"
    #     if "DT_NASC" not in df.columns:
    #         df["DT_NASC"] = None
    #     else:
    #         df["DT_NASC"] = pd.to_datetime(df["DT_NASC"], errors="coerce").strftime("%Y-%m-%dT%H:%M:%S.000Z")
    #         # "IDADE"
    #         hoje = datetime.today()
    #         df["IDADE"] = (
    #             (hoje - df["DT_NASC"]).dt.days / 365.25
    #         ).round().astype("Int64")
        
    #     # "DT_SIN_PRI","DT_NOTIFIC" 
    #     df["DT_SIN_PRI"] = df["DT_SIN_PRI"].apply(string_to_iso_utc)
    #     df["DT_NOTIFIC"] = df["DT_NOTIFIC"].apply(string_to_iso_utc)
    #     #---------------------

        
    #     # --- Criação do Endereço Completo ---
    #     # "MUNICIPIO RESIDÊNCIA"
    #     # "ENDEREÇO COMPLETO"
    #     df["ENDEREÇO COMPLETO"] = (
    #         df[["NM_BAIRRO", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM"]]
    #         .fillna("")
    #         .agg(", ".join, axis=1)
    #         .str.strip(", ")
    #     )
    #     # ---------------------
    
    #     print(df)
    #     logger.info("Tratamento padrão dos dados concluído")
    #     #df = df.fillna("")

    #     # # --- Arrumar Municipio de Residencia ---
    #     # dic_mun_res = pd.read_excel("Dic_Mun_Res.xlsx")
    #     # tabela_merge = pd.merge(df, dic_mun_res, on="ID_MN_RESI", how="left")

    #     # # --- Arrumar Municipio de Notificação ---
    #     # dic_mun_not = pd.read_excel("Dic_Mun_NOT.xlsx")
    #     # tabela_merge2 = pd.merge(tabela_merge, dic_mun_not, on="ID_MUNICIP", how="left")

    #     # --- Substituir NAs por string vazia ---
    #     #tabela_merge2 = tabela_merge2.fillna("")

    #     #tabela_merge2.to_csv(caminho_arquivo, index=False)

    #     return df