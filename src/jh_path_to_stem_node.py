from pathlib import Path


class JHPathToStemNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING",),
            },
        }

    RETURN_TYPES: tuple[str] = ("STRING",)
    FUNCTION = "path_to_stem"
    CATEGORY = "XMP Metadata Nodes/Utilities"
    OUTPUT_NODE = False

    def path_to_stem(self, path: str) -> tuple[str]:
        return (Path(path).stem,)
