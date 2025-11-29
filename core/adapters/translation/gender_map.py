from .translation_registry import translation_registry

GENDER_MAP = {
    "M": "LNG_REFERENCE_DATA_CATEGORY_GENDER_MALE",
    "F": "LNG_REFERENCE_DATA_CATEGORY_GENDER_FEMALE",
}

translation_registry.register("gender", GENDER_MAP)
