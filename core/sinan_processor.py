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

class SinanDataProcessor(BaseProcessor):
    def __init__(self, disease_processor: BaseProcessor):
        self.disease_processor = disease_processor
    
    # =====================================================
    # === MÉTODO PRINCIPAL ================================
    # =====================================================

    def _disease_data_treatment(self, df: pd.DataFrame) -> pd.DataFrame:
        ## TODO: rodar o tratamento específico da doença aqui
        return df

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._standard_data_treatment(df)
        logger.info("Iniciando processamento específico da doença")
        df = self.disease_processor.run(df)
        df = self._disease_data_treatment(df)
        logger.info("Processamento específico da doença concluído")
        return df
    
    # =====================================================
    # === TRATAMENTO PADRÃO ===============================
    # =====================================================
    def _standard_data_treatment(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Iniciando tratamento padrão dos dados")

        df = df.copy()
        #remover linhas sem numero de notificacao
        df = df.dropna(subset=["NU_NOTIFIC"])
        #remover valores nan
        df = df.fillna("")
        
        #traduzindo dados do csv para palavras-chave do godata
        self._translate_keywords(df)
        
        #processar dados especificos
        self._process_birth_date(df)
        self._process_notification_dates(df)
        self._build_full_address(df)
        
        #inserir timestamp de atualizacao
        self._insert_timestamp(df)

        logger.info("Tratamento padrão dos dados concluído")
        return df

    # =====================================================
    # === MÉTODOS AUXILIARES ==============================
    # =====================================================
    def _translate_keywords(self, df: pd.DataFrame) -> None:
        normalization_map = {
            "CS_SEXO": {
                "mapper": self._map_generic,
                "registry_key": "gender",
            },
            "CS_GESTANT": {
                "mapper": self._map_generic,
                "registry_key": "pregnancy_status",
                "default": TranslationRegistry.get("pregnancy_status").get("9", ""),
            },
            "ID_CNS_SUS": {
                "mapper": self._map_document_type,
            },
            "CLASSIFICAÇÃO FINAL": {
                "mapper": self._map_generic,
                "registry_key": "classification",
            },
            "Endereço_Atual": {
                "default": TranslationRegistry.get("address_type").get("Endereço Atual", "")
            },
            "ID_CNS_SUS": {
                "mapper": self._map_document_type,
                "target": "TIPO DE DOCUMENTO",
                "registry_key": "document_type",
            },
        }

        for col, cfg in normalization_map.items():
            if col not in df.columns:
                continue
            
            if "mapper" in cfg:
                newvalue = df[col].apply(
                    lambda v: 
                        cfg["mapper"](
                            v,
                            cfg.get("registry_key"),
                        cfg.get("default", ""),
                    )
                )
            else:
                newvalue = cfg["default"]
            
            if "target" in cfg:
                df[cfg["target"]] = newvalue
            else: 
                df[col] = newvalue

    def _map_generic(self, value: str, registry_key: str, default: str = "") -> str:
        mapping = TranslationRegistry.get(registry_key)
        return mapping.get(value, default)

    def _map_document_type(self, value: str, registry_key:str, default: str = "") -> str:
        mapping = TranslationRegistry.get(registry_key)
        return (
            mapping.get("CNS") if str(value).strip() != "" else default
        )
  
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

    
    #     #------ não precisa de tratamento ------------  ----
    #     # (dados pessoais)- talvez garantir que não fique nulo
    #     # "NM_PACIENT", "NU_CEP", "NU_TELEFON","ID_CNS_SUS" 
    #     # ------------------------------------------------
        