import pandas as pd

class ResidenceMapper:
    """
    Classe para mapear códigos de município e UF (unidade federativa)
    para seus respectivos nomes, com base em um dicionário Excel.
    """
    def __init__(self, dictionary_path: str):
        dic = pd.read_excel(dictionary_path, dtype=str)
        dic.columns = dic.columns.str.strip().str.upper()
        
        expected_cols = {"ID_MN_RESI", "MUNICIPIO RESI", "UF RESI"}
        missing = expected_cols - set(dic.columns)
        if missing:
            raise ValueError(f"Colunas ausentes no dicionário: {missing}")

        # Dicionário de código → município
        self.municipios = (
            dic[["ID_MN_RESI", "MUNICIPIO RESI"]]
            .drop_duplicates()
            .set_index("ID_MN_RESI")["MUNICIPIO RESI"]
            .to_dict()
        )

        # Dicionário de código → UF
        self.ufs = (
            dic[["ID_MN_RESI", "UF RESI"]]
            .drop_duplicates()
            .set_index("ID_MN_RESI")["UF RESI"]
            .to_dict()
        )
    
    def get_municipio(self, codigo: str) -> str:
        """Retorna o nome do município dado o código."""
        return self.municipios.get(codigo, "")
    
    def get_uf(self, codigo: str) -> str:
        """Retorna o nome da UF dado o código."""
        return self.ufs.get(codigo, "")
    

