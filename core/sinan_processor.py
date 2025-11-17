from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime

from .logger import logger
from .utils import string_to_iso_utc
from .mappers.translation_registry import TranslationRegistry
from .mappers.location_id_mapper import LocationIdMapper
class Processor(ABC):
    @abstractmethod
    def run(self, df: pd.DataFrame) -> pd.DataFrame :
        pass

class SinanDataProcessor(Processor):
    def __init__(self, residence_mapper: LocationIdMapper):
        # =====================================================
        # === CONFIGURAÇÕES DE TRADUÇÕES ======================
        # =====================================================
        self.translations = {
            "CS_SEXO": {
                "mapping": lambda x: TranslationRegistry.translate("gender", x),
            },
            "CS_GESTANT": {
                "mapping": lambda x: TranslationRegistry.translate("pregnancy", x),
            },
            "CLASSIFICAÇÃO FINAL": {
                "mapping": lambda x: TranslationRegistry.translate("classification", x),
            },
            "TIPO DE DOCUMENTO": {
                "mapping": lambda x: TranslationRegistry.translate("document_type", "CNS") if x else None,
                "source_column": "ID_CNS_SUS",
            },
            "Endereço_Atual": {
                "mapping": lambda x: TranslationRegistry.translate("address_type", "Endereço Atual"),
            },
            "MUNICIPIO RESIDÊNCIA": {
                "mapping": lambda x: residence_mapper.get_municipio(x),
                "source_column": "ID_MN_RESI",
            },
            "UF RESIDÊNCIA": {
                "mapping": lambda x: residence_mapper.get_uf(x),
                "source_column": "ID_MN_RESI",
            },
        }

        # =====================================================
        # === CONFIGURAÇÕES DE OUTROS TRATAMENTOS =============
        # =====================================================
        self.treatments = {
            "DT_NASC": self._process_birth_date,
            "IDADE": self._calculate_age,
            "DT_SIN_PRI": self._convert_date_iso,
            "DT_NOTIFIC": self._convert_date_iso,
            "ENDEREÇO COMPLETO": self._build_full_address,
            "Atualizado_em": self._insert_timestamp,
        }

    # =====================================================
    # === MÉTODO PRINCIPAL ================================
    # =====================================================
    def run(self, df: pd.DataFrame, anonymous_data=False) -> pd.DataFrame:
        logger.info("Iniciando tratamento padrão dos dados")

        # Etapa 0: pré-processamento
        self._preprocess(df, anonymous_data=anonymous_data)

        # Etapa 1: traduções
        self._apply_translations(df)

        # Etapa 2: tratamentos definidos
        for col, func in self.treatments.items():
            if func.__code__.co_argcount > 2:
                func(df, col)
            else:
                func(df)

        logger.info("Tratamento padrão dos dados concluído")
        return df


    # =====================================================
    # === PRÉ-PROCESSAMENTO ===============================
    # =====================================================
    def _preprocess(self, df: pd.DataFrame, anonymous_data: bool = False) -> None:
        # 1. Normalizar valores ausentes
        mask = df.isin(["NA", ""])
        df.where(~mask, pd.NA, inplace=True)
        #df.fillna("", inplace=True)

        # 2. Garantir que as colunas existem
        personal_cols = ["NM_PACIENT", "NU_CEP", "NU_TELEFON", "ID_CNS_SUS", "Endereço_Atual"]
        for col in personal_cols:
            if col not in df.columns:
                df[col] = ""

        # 3. Anonimização (se solicitada)
        if anonymous_data:
            placeholder_values = {
                "NM_PACIENT": "Paciente Anônimo",
                "NU_CEP": "00000-000",
                "NU_TELEFON": "(00)0000-0000",
                "ID_CNS_SUS": "000000000000000",
                "DT_NASC": datetime(2000, 1, 1),
            }
            for col, value in placeholder_values.items():
                df[col] = value


    # =====================================================
    # === TRATAMENTO DE TRADUÇÕES =========================
    # =====================================================
    def _apply_translations(self, df: pd.DataFrame) -> None:
        for target_col, cfg in self.translations.items():
            mapping = cfg["mapping"]
            source_col = cfg.get("source_column", target_col)

            df[target_col] = df[source_col].apply(mapping)


    # =====================================================
    # === TRATAMENTOS DE DATAS =============================
    # =====================================================
    def _convert_date_iso(self, df: pd.DataFrame, col: str) -> None:
        if col in df.columns:
            df[col] = df[col].apply(string_to_iso_utc)


    def _process_birth_date(self, df: pd.DataFrame, col="DT_NASC") -> None:
        if col not in df.columns:
            df[col] = ""
            return
        df[col] = pd.to_datetime(df[col], errors="coerce")
        #df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        
    def _process_age(self, df: pd.DataFrame, col="IDADE") -> None:
        birthday_col = "DT_NASC"
        if birthday_col not in df.columns:
            df[col] = pd.NA
            return

        df[col] = df[birthday_col].apply(self._calculate_age)


    def _calculate_age(self, birth_date) -> int:
        if not isinstance(birth_date, (pd.Timestamp, datetime)):
            try:
                birth_date = pd.to_datetime(birth_date, errors="coerce")
            except Exception:
                return pd.NA
            
        today = pd.Timestamp.today()
        delta = today - birth_date
        return int(round(delta.days / 365.25))


    # =====================================================
    # === COMPOSIÇÃO DE CAMPOS =============================
    # =====================================================
    def _build_full_address(self, df: pd.DataFrame, col="ENDEREÇO COMPLETO") -> None:
        required_cols = ["NM_BAIRRO", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM"]
        for c in required_cols:
            if c not in df.columns:
                df[c] = ""
        df[col] = df[required_cols].fillna("").agg(", ".join, axis=1).str.strip(", ")


    # =====================================================
    # === CAMPOS DE METADADOS ==============================
    # =====================================================
    def _insert_timestamp(self, df: pd.DataFrame, col="Atualizado_em") -> None:
        df[col] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")