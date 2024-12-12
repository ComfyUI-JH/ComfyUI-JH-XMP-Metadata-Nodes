from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.resolve()))

from src.jh_format_instructions_node import JHFormatInstructionsNode
from src.jh_path_to_stem import JHPathToStem
from src.jh_save_image_with_xmp_metadata_node import JHSaveImageWithXMPMetadataNode
from src.jh_get_widget_value_node import JHGetWidgetValueNode

NODE_CLASS_MAPPINGS = {
    "JHFormatInstructionsNode": JHFormatInstructionsNode,
    "JHPathToStem": JHPathToStem,
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadataNode,
    "JHGetWidgetValueNode": JHGetWidgetValueNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JHFormatInstructionsNode": "Format Instructions",
    "JHPathToStem": "Path to Stem",
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
    "JHGetWidgetValueNode": "Get Widget Value",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
