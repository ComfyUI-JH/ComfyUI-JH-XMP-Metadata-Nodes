from pathlib import Path


class JHPathToStem:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "path_to_stem"
    CATEGORY = "XMP Metadata Nodes/Utilities"
    OUTPUT_NODE = False

    def path_to_stem(self, path):
        return (Path(path).stem,)