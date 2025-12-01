import pandas as pd
from typing import Optional
from core.logger import logger
from core.domain.ports import DataframeReader

class XlsxReader(DataframeReader):
    def __init__(self,file_path: str, n_rows: Optional[int] = None):
        self.file_path = file_path
        self.n_rows = n_rows

    def read_dataframe(self) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.file_path, nrows=self.n_rows,dtype=str)
            logger.info("XLSX lido com sucesso: %s linhas", len(df))
        except Exception as e:
            logger.error("Erro ao ler o XLSX: %s", e)
            raise

        return df