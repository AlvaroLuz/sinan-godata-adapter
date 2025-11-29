from .translation_registry import translation_registry

DOCUMENT_MAP = {
    "CNS": "LNG_REFERENCE_DATA_CATEGORY_DOCUMENT_TYPE_CNS",
    "CPF": "LNG_REFERENCE_DATA_CATEGORY_DOCUMENT_TYPE_CPF",
    "Other": "LNG_REFERENCE_DATA_CATEGORY_DOCUMENT_TYPE_OTHER",
    "": "",
}

translation_registry.register("document_type", DOCUMENT_MAP)