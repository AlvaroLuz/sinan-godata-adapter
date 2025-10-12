from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class QuestionnaireAnswers:    
    resultado_rubeola_S2_igg: Optional[str] 
    resultado_rubeola_S2_igm: Optional[str] 
    resultado_sarampo_s2_igg: Optional[str] 
    resultado_sarampo_s2_igm: Optional[str] 
    resultado_rubeola_s1_igg: Optional[str] 
    resultado_rubeola_s_1_ig_m_: Optional[str] 
    resultado_sarampo_s1_igg: Optional[str] 
    resultado_sarampo_s_1_ig_m_: Optional[str] 
    contato_com_caso_suspeito_ou_confirmado_de_sarampo_ou_rubeola_ate_23_dias_antes_do_inicio_dos_sinais_e_sintomas: Optional[str] 
    tomou_vacina_contra_sarampo_e_rubeola_dupla_triplice_viral_e_tetraviral: Optional[str] 
    nome_da_mae: Optional[str] 
    municipio_de_notificacao: Optional[str]
    data_da_coleta_s_1: Optional[datetime]
    data_da_coleta_s_2: Optional[datetime]
    data_do_inicio_da_febre: Optional[datetime]
    data_do_inicio_do_enxantema_manchas_vermelhas_pelo_corpo: Optional[datetime]


QUESTIONNAIRE_MAPPING = {
    "resultado_rubeola_S2_igg": "ID_S2_IGG_",
    "resultado_rubeola_S2_igm": "ID_S2_IGM_",
    "resultado_sarampo_s2_igg": "ID_S2_IGG",
    "resultado_sarampo_s2_igm": "ID_S2_IGM",
    "data_da_coleta_s_2": "DT_COL_2",
    "resultado_rubeola_s1_igg": "ID_S1_IGG_",
    "resultado_rubeola_s_1_ig_m_": "ID_S1_IGM_",
    "resultado_sarampo_s1_igg": "ID_S1_IGG",
    "resultado_sarampo_s_1_ig_m_": "ID_S1_IGM_",
    "data_da_coleta_s_1": "DT_COL_1",
    "contato_com_caso_suspeito_ou_confirmado_de_sarampo_ou_rubeola_ate_23_dias_antes_do_inicio_dos_sinais_e_sintomas": "CS_FONTE",
    "tomou_vacina_contra_sarampo_e_rubeola_dupla_triplice_viral_e_tetraviral": "CS_VACINA",
    "data_do_inicio_da_febre": "DT_FEBRE",
    "data_do_inicio_do_enxantema_manchas_vermelhas_pelo_corpo": "DT_INICIO_",
    "nome_da_mae": "NM_MAE_PAC",
    "municipio_de_notificacao": "MUNICIPIO NOTIFICAÇÃO"    
}

