from .translation_registry import translation_registry

ADDRESS_TYPE_MAP = lambda x : "LNG_REFERENCE_DATA_CATEGORY_ADDRESS_TYPE_USUAL_PLACE_OF_RESIDENCE"

translation_registry.register(name="address_type",mapping=ADDRESS_TYPE_MAP)