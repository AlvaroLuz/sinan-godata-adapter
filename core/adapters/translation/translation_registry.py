from typing import Callable, Dict, Any


class TranslationRegistry:
    def __init__(self):
        # Ex: {"gender": translator_fn}
        self._registry: Dict[str, Callable[[Any], Any]] = {}

    def register(self, name: str, translator: Callable[[Any], Any]):
        """
        Registra um tradutor no registry.

        Tradutores podem ser:
        - um map/dict simples
        - um callable
        """
        if isinstance(translator, dict):
            translator = self._wrap_dict_translator(translator)

        if not callable(translator):
            raise ValueError(f"Translator for '{name}' is not callable or dict.")

        self._registry[name] = translator

    def translate(self, name: str, value: Any) -> Any:
        """
        Aplica o tradutor adequado.
        Se não existir, retorna o valor original.
        """
        translator = self._registry.get(name)
        if translator is None:
            return value
        return translator(value)

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
