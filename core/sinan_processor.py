from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime

from .logger import logger
from .utils import string_to_iso_utc
from .mappers.translation_registry import TranslationRegistry

class Processor(ABC):
    @abstractmethod
    def run(self, df: pd.DataFrame) -> pd.DataFrame :
        pass

class SinanDataProcessor(Processor):
     
    # =====================================================
    # === MÉTODO PRINCIPAL ================================
    # =====================================================

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
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
                "registry_key": "gender",
            },
            "CS_GESTANT": {
                "registry_key": "pregnancy_status",
            },
            "CLASSIFICAÇÃO FINAL": {
                "registry_key": "classification",
            },
            
        }

        for col, cfg in normalization_map.items():
            if col not in df.columns:
                continue
        
            newvalue = df[col].apply(
                lambda value: TranslationRegistry.translate(cfg["registry_key"], value)
            )

            if "target" in cfg:
                df[cfg["target"]] = newvalue
            else: 
                df[col] = newvalue
        
        df["Endereço_Atual"] = TranslationRegistry.translate("address_type", "Endereço Atual")
        
        df["TIPO DE DOCUMENTO"] = df["ID_CNS_SUS"].apply(
            lambda x: 
                pd.NA if x=="" else  TranslationRegistry.translate("document_type", "CNS")
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
        