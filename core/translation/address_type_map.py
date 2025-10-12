from .registry import TranslationRegistry

ADDRESS_TYPE_MAP = {
    "Endereço Atual": "LNG_REFERENCE_DATA_CATEGORY_ADDRESS_TYPE_USUAL_PLACE_OF_RESIDENCE",
    "": ""
}

TranslationRegistry.register("address_type", ADDRESS_TYPE_MAP)