from .translation_registry import TranslationRegistry

DOCUMENT_MAP = {
    "CNS": "LNG_REFERENCE_DATA_CATEGORY_DOCUMENT_TYPE_CNS",
    "CPF": "LNG_REFERENCE_DATA_CATEGORY_DOCUMENT_TYPE_CPF",
    "Other": "LNG_REFERENCE_DATA_CATEGORY_DOCUMENT_TYPE_OTHER",
}

TranslationRegistry.register("document_type", DOCUMENT_MAP, default_value=DOCUMENT_MAP["CNS"])