from pathlib import Path

from comfyui_jh_xmp_metadata_nodes import jh_types


class JHPathToStemNode:
    @classmethod
    def INPUT_TYPES(cls) -> jh_types.JHInputTypesType:
        return {
            "required": {
                "path": (jh_types.JHNodeInputOutputTypeEnum.STRING, {}),
            },
        }

    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.STRING,)
    FUNCTION = "path_to_stem"
    CATEGORY = "XMP Metadata Nodes/Utilities"
    OUTPUT_NODE = False

    def path_to_stem(self, path: str) -> tuple[str]:
        return (Path(path).stem,)
