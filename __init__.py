"""
This module initializes the `ComfyUI_XMPMetadataNodes` package by defining
mappings for custom node classes and their display names. These mappings
enable the integration of custom nodes, such as those for formatting
instructions, handling XMP metadata, and processing file paths, into the
ComfyUI framework.
"""

# pylint: disable=wrong-import-position
# pylint: disable=invalid-name

import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent.resolve()))

from src.jh_format_instructions_node import JHFormatInstructionsNode
from src.jh_get_widget_value_nodes import (
    JHGetWidgetValueFloatNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueStringNode,
)
from src.jh_load_image_with_xmp_metadata_node import JHLoadImageWithXMPMetadataNode
from src.jh_path_to_stem_node import JHPathToStemNode
from src.jh_save_image_with_xmp_metadata_node import JHSaveImageWithXMPMetadataNode

NODE_CLASS_MAPPINGS: dict[str, Any] = {
    "JHFormatInstructionsNode": JHFormatInstructionsNode,
    "JHPathToStemNode": JHPathToStemNode,
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadataNode,
    "JHLoadImageWithXMPMetadataNode": JHLoadImageWithXMPMetadataNode,
    "JHGetWidgetValueStringNode": JHGetWidgetValueStringNode,
    "JHGetWidgetValueIntNode": JHGetWidgetValueIntNode,
    "JHGetWidgetValueFloatNode": JHGetWidgetValueFloatNode,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "JHFormatInstructionsNode": "Format Instructions",
    "JHPathToStemNode": "Path to Stem",
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
    "JHLoadImageWithXMPMetadataNode": "Load Image With XMP Metadata",
    "JHGetWidgetValueStringNode": "Get Widget Value (String)",
    "JHGetWidgetValueIntNode": "Get Widget Value (Integer)",
    "JHGetWidgetValueFloatNode": "Get Widget Value (Float)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
