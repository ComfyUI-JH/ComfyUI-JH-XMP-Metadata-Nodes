from .jh_save_image_with_xmp_metadata import JHSaveImageWithXMPMetadata

NODE_CLASS_MAPPINGS = {
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadata,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]