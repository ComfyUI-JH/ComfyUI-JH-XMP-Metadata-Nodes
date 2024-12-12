from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.resolve()))

from src.jh_path_to_stem import JHPathToStem
from src.jh_save_image_with_xmp_metadata_node import JHSaveImageWithXMPMetadataNode

NODE_CLASS_MAPPINGS = {
    "JHPathToStem": JHPathToStem,
    "JHSaveImageWithXMPMetadata": JHSaveImageWithXMPMetadataNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JHPathToStem": "Path to Stem",
    "JHSaveImageWithXMPMetadata": "Save Image With XMP Metadata",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]