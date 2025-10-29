from typing import Any, Optional

class TranslationRegistry:
    _registry = {}
    _default_value = {}

    @classmethod
    def register(cls, name: str, mapping: dict, default_value: Optional[str] = None):
        cls._registry[name] = mapping
        cls._default_value[name] = default_value

    @classmethod
    def get(cls, name: str) -> dict:
        return cls._registry.get(name, {})
    
    @classmethod
    def translate(self, name: str, value: Any) -> Any:
        """Traduz um valor usando o tradutor registrado."""
        translator = self._registry.get(name)
        if translator is None:
            return value  # fallback: retorna o próprio valor
        if callable(translator):
            return translator(value)
        return translator.get(value, self._default_value.get(name))
    
    @classmethod
    def all(cls) -> dict:
        return cls._registry