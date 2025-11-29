import importlib
import pkgutil
from dataclasses import is_dataclass
from typing import Dict, Type, Any
from core.adapters.translation.translation_registry import translation_registry

class DiseaseModuleSpec:
    """
    Container simples para representar o módulo carregado.
    """
    def __init__(
        self,
        name: str,
        questionnaire_cls: Type[Any],
        questionnaire_map: Dict[str, str],
        case_classification_map: Dict[str, Any],
        outcome_map: Dict[str, Any],
    ):
        self.name = name
        self.questionnaire_cls = questionnaire_cls
        self.questionnaire_map = questionnaire_map

        ## Registrando tradutores globais para outcome e case_classification
        translation_registry.register(
            f"{name}_case_classification", case_classification_map
        )
        translation_registry.register(f"{name}_outcome", outcome_map)
        



class DiseaseRegistry:
    """
    Carrega dinamicamente todos módulos dentro do pacote disease_modules.
    Cada módulo deve conter:
      - QuestionnaireAnswers
      - QUESTIONNAIRE_MAP
      - CASE_CLASSIFICATION_MAP
      - OUTCOME_MAP
    """

    def __init__(self, module_package: str = "core.domain.diseases.modules"):
        self.module_package = module_package
        self._registry: Dict[str, DiseaseModuleSpec] = {}
        self.load_all_modules()

    # ----------------------------------------------------------------------
    def load_all_modules(self):
        """
        Vasculha automaticamente o pacote e registra cada módulo válido.
        """
        package = importlib.import_module(self.module_package)

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full_path = f"{self.module_package}.{module_name}"

            mod = importlib.import_module(full_path)

            # Identificar os quatro componentes obrigatórios -------------------
            q_cls = getattr(mod, "QuestionnaireAnswers", None)
            questionnaire_map = getattr(mod, "QUESTIONNAIRE_MAP", None)
            case_classification_map = getattr(mod, "CASE_CLASSIFICATION_MAP", None)
            outcome_map = getattr(mod, "OUTCOME_MAP", None)

            if (
                q_cls is None
                or questionnaire_map is None
                or case_classification_map is None
                or outcome_map is None
                or case_classification_map is None
                or outcome_map is None
                or not is_dataclass(q_cls)
            ):
                # Se o módulo não tiver a estrutura necessária, ignore.
                continue

            # Registrar -------------------------------------------------------
            self._registry[module_name] = DiseaseModuleSpec(
                name=module_name,
                questionnaire_cls=q_cls,
                questionnaire_map=questionnaire_map,
                case_classification_map=case_classification_map,
                outcome_map=outcome_map,
            )

    # ----------------------------------------------------------------------
    def get(self, name: str) -> DiseaseModuleSpec:
        """
        Retorna o módulo registrado (ex: "sarampo").
        """
        if name not in self._registry:
            raise KeyError(f"Módulo de doença '{name}' não encontrado no registry.")
        return self._registry[name]

    # ----------------------------------------------------------------------
    def list_modules(self):
        """
        Lista todas as doenças registradas.
        """
        return list(self._registry.keys())
    
# Singleton global do registry
disease_registry = DiseaseRegistry()