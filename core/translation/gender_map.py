from .registry import TranslationRegistry

GENDER_MAP = {
    "M": "LNG_REFERENCE_DATA_CATEGORY_GENDER_MALE",
    "F": "LNG_REFERENCE_DATA_CATEGORY_GENDER_FEMALE",
    "": "",
}

TranslationRegistry.register("gender", GENDER_MAP)
