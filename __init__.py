from typing import Any

from .src.jh_format_metadata_node import JHFormatMetadataNode
from .src.jh_get_widget_value_nodes import (
    JHGetWidgetValueFloatNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueStringNode,
)
from .src.jh_load_image_with_xmp_metadata_node import JHLoadImageWithXMPMetadataNode
from .src.jh_path_to_stem_node import JHPathToStemNode
from .src.jh_save_image_with_xmp_metadata_node import JHSaveImageWithXMPMetadataNode

NODE_CLASS_MAPPINGS: dict[str, Any] = {
    "JHFormatMetadataNode": JHFormatMetadataNode,
    "JHPathToStemNode": JHPathToStemNode,
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadataNode,
    "JHLoadImageWithXMPMetadataNode": JHLoadImageWithXMPMetadataNode,
    "JHGetWidgetValueStringNode": JHGetWidgetValueStringNode,
    "JHGetWidgetValueIntNode": JHGetWidgetValueIntNode,
    "JHGetWidgetValueFloatNode": JHGetWidgetValueFloatNode,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "JHFormatMetadataNode": "Format Metadata",
    "JHPathToStemNode": "Path to Stem",
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
    "JHLoadImageWithXMPMetadataNode": "Load Image With XMP Metadata",
    "JHGetWidgetValueStringNode": "Get Widget Value (String)",
    "JHGetWidgetValueIntNode": "Get Widget Value (Integer)",
    "JHGetWidgetValueFloatNode": "Get Widget Value (Float)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
