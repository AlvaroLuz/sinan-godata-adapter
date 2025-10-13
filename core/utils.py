from datetime import datetime, timezone, timedelta
import re

def string_to_iso_utc(date_str: str) -> str:
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
        date_str = date_str.strip()
        
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