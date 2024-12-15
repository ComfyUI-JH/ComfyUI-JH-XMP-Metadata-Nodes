from pathlib import Path
from typing import Literal


class JHPathToStemNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING",),
            },
        }

    RETURN_TYPES: tuple[Literal["STRING"]] = ("STRING",)
    FUNCTION = "path_to_stem"
    CATEGORY = "XMP Metadata Nodes/Utilities"
    OUTPUT_NODE = False

    def path_to_stem(self, path) -> tuple[str]:
        return (Path(path).stem,)
