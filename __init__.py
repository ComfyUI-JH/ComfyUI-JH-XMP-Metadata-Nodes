from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.resolve()))

from src.jh_format_instructions_node import JHFormatInstructionsNode
from src.jh_path_to_stem_node import JHPathToStemNode
from src.jh_save_image_with_xmp_metadata_node import JHSaveImageWithXMPMetadataNode
from src.jh_get_widget_value_nodes import (
    JHGetWidgetValueStringNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueFloatNode,
)


NODE_CLASS_MAPPINGS = {
    "JHFormatInstructionsNode": JHFormatInstructionsNode,
    "JHPathToStemNode": JHPathToStemNode,
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadataNode,
    "JHGetWidgetValueStringNode": JHGetWidgetValueStringNode,
    "JHGetWidgetValueIntNode": JHGetWidgetValueIntNode,
    "JHGetWidgetValueFloatNode": JHGetWidgetValueFloatNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JHFormatInstructionsNode": "Format Instructions",
    "JHPathToStemNode": "Path to Stem",
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
    "JHGetWidgetValueStringNode": "Get Widget Value (String)",
    "JHGetWidgetValueIntNode": "Get Widget Value (Integer)",
    "JHGetWidgetValueFloatNode": "Get Widget Value (Float)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
