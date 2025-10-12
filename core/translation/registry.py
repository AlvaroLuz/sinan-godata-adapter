class TranslationRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, mapping: dict):
        cls._registry[name] = mapping

    @classmethod
    def get(cls, name: str) -> dict:
        return cls._registry.get(name, {})

    @classmethod
    def all(cls) -> dict:
        return cls._registry