from typing import Callable, Dict, Any


class TranslationRegistry:
    def __init__(self):
        # Ex: {"gender": translator_fn}
        self._registry: Dict[str, Callable[[Any], Any]] = {}

    
    def register(self, name: str, mapping: Callable[[Any], Any]):
        """
        Registra um tradutor no registry.

        Tradutores podem ser:
        - um map/dict simples
        - um callable
        """
        if isinstance(mapping, dict):
            mapping = self._wrap_dict_translator(mapping)

        if not callable(mapping):
            raise ValueError(f"Translator for '{name}' is not callable or dict.")

        self._registry[name] = mapping

    def translate(self, name: str, value: Any) -> Any:
        """
        Aplica o tradutor adequado.
        Se não existir, retorna o valor original.
        """
        mapping = self._registry.get(name)
        if mapping is None:
            return value
        return mapping(value)

    @staticmethod
    def _wrap_dict_translator(mapper: Dict[Any, Any]):
        """
        Transforma um dict em uma função.
        """
        def fn(value):
            return mapper.get(value, value)
        return fn


# Instância global (opcional e prática)
translation_registry = TranslationRegistry()
