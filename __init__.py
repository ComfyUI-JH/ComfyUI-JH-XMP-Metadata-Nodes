from .jh_save_image_with_xmp_metadata import JHSaveImageWithXMPMetadata
from .jh_save_png_with_xmp_metadata import JHSavePNGWithXMPMetadata
from .jh_save_webp_with_xmp_metadata import JHSaveWebPWithXMPMetadata

NODE_CLASS_MAPPINGS = {
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadata,
    "JHSavePNGWithXMPMetadata": JHSavePNGWithXMPMetadata,
    "JHSaveWebPWithXMPMetadata": JHSaveWebPWithXMPMetadata,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
    "JHSavePNGWithXMPMetadata": "Save PNG With XMP Metadata",
    "JHSaveWebPWithXMPMetadata": "Save WebP With XMP Metadata",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]