from pathlib import Path
from unittest.mock import MagicMock

from comfyui_jh_xmp_metadata_nodes import jh_types

try:
    import folder_paths  # pyright: ignore[reportMissingImports]
except ImportError:
    folder_paths = MagicMock()


class JHFormatCivitaiMetadataNode:
    @classmethod
    def INPUT_TYPES(cls) -> jh_types.JHInputTypesType:
        # fmt: off
        return {
            "required": {},
            "optional": {
                "prompt": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "defaultInput": True
                    },
                ),
                "negative_prompt": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "defaultInput": True
                    },
                ),
                "seed": (
                    jh_types.JHNodeInputOutputTypeEnum.INT,
                    {
                        "defaultInput": True
                    }
                ),
                "sampler_name": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "defaultInput": True
                    },
                ),
                "scheduler_name": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "defaultInput": True
                    },
                ),
                "steps": (
                    jh_types.JHNodeInputOutputTypeEnum.INT,
                    {
                        "defaultInput": True
                    }
                ),
                "cfg": (
                    jh_types.JHNodeInputOutputTypeEnum.FLOAT,
                    {
                        "defaultInput": True
                    }
                ),
                "guidance": (
                    jh_types.JHNodeInputOutputTypeEnum.FLOAT,
                    {
                        "defaultInput": True
                    }
                ),
                "model_path": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "defaultInput": True
                    }
                ),
                "width": (
                    jh_types.JHNodeInputOutputTypeEnum.INT,
                    {
                        "defaultInput": True
                    }
                ),
                "height": (
                    jh_types.JHNodeInputOutputTypeEnum.INT,
                    {
                        "defaultInput": True
                    }
                ),
            },
        }
        # fmt: on

    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.STRING,)
    FUNCTION = "format_metadata"
    CATEGORY = "XMP Metadata Nodes"

    def format_metadata(
        self,
        prompt: str | None = None,
        negative_prompt: str | None = None,
        seed: int | None = None,
        sampler_name: str | None = None,
        scheduler_name: str | None = None,
        steps: int | None = None,
        cfg: float | None = None,
        guidance: float | None = None,
        model_path: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> tuple[str]:
        if model_path is not None:
            possible_locations = ["checkpoints", "diffusion_models", "unet"]
            for location in possible_locations:
                full_model_path = folder_paths.get_full_path(location, model_path)
                if full_model_path is not None:
                    model_path = full_model_path
                    break

        model_stem = None
        if model_path is not None:
            model_stem = Path(model_path).stem

        last_line_parts = []

        if steps is not None:
            last_line_parts.append(f"Steps: {steps}")

        if sampler_name is not None:
            if scheduler_name == "normal":
                last_line_parts.append(f"Sampler: {sampler_name}")
            else:
                last_line_parts.append(f"Sampler: {sampler_name}_{scheduler_name}")

        if cfg is not None:
            last_line_parts.append(f"CFG Scale: {cfg}")

        if guidance is not None:
            last_line_parts.append(f"Guidance: {guidance}")

        if seed is not None:
            last_line_parts.append(f"Seed: {seed}")

        if width is not None and height is not None:
            last_line_parts.append(f"Size: {width}x{height}")

        if model_stem is not None:
            last_line_parts.append(f"Model: {model_stem}")

        last_line = ", ".join(last_line_parts)

        formatted_string = ""
        formatted_string += f"{prompt}\n"
        formatted_string += f"Negative prompt: {negative_prompt}\n"
        formatted_string += f"{last_line}"

        return (formatted_string,)
