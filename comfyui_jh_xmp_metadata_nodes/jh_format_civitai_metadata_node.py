from enum import StrEnum
from pathlib import Path
from unittest.mock import MagicMock

from comfyui_jh_xmp_metadata_nodes import jh_types

try:
    import folder_paths  # pyright: ignore[reportMissingImports]
except ImportError:
    folder_paths = MagicMock()


class JHCivitaiSamplerEnum(StrEnum):
    EULER_A = "Euler a"
    EULER = "Euler"
    LMS = "LMS"
    HEUN = "Heun"
    DPM2 = "DPM2"
    DPM2_A = "DPM2 a"
    DPMPP_2S_A = "DPM++ 2S a"
    DPMPP_2M = "DPM++ 2M"
    DPMPP_SDE = "DPM++ SDE"
    DPMPP_2M_SDE = "DPM++ 2M SDE"
    DPMPP_3M_SDE = "DPM++ 3M SDE"
    DPM_FAST = "DPM fast"
    DPM_ADAPTIVE = "DPM adaptive"
    LMS_KARRAS = "LMS Karras"
    DPM2_KARRAS = "DPM2 Karras"
    DPM2_A_KARRAS = "DPM2 a Karras"
    DPMPP_2S_A_KARRAS = "DPM++ 2S a Karras"
    DPMPP_2M_KARRAS = "DPM++ 2M Karras"
    DPMPP_SDE_KARRAS = "DPM++ SDE Karras"
    DPMPP_2M_SDE_KARRAS = "DPM++ 2M SDE Karras"
    DPMPP_3M_SDE_KARRAS = "DPM++ 3M SDE Karras"
    DPMPP_3M_SDE_EXPONENTIAL = "DPM++ 3M SDE Exponential"
    DDIM = "DDIM"
    PLMS = "PLMS"
    UNIPC = "UniPC"
    LCM = "LCM"


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
            pretty_sampler_name = f"{sampler_name}_{scheduler_name}"
            match sampler_name:
                case "euler" | "euler_cfg_pp":
                    pretty_sampler_name = JHCivitaiSamplerEnum.EULER
                case "euler_ancestral" | "euler_ancestral_cfg_pp":
                    pretty_sampler_name = JHCivitaiSamplerEnum.EULER_A
                case "heun" | "heunpp2":
                    pretty_sampler_name = JHCivitaiSamplerEnum.HEUN
                case "dpm_2":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPM2
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPM2_KARRAS
                case "dpm_2_ancestral":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPM2_A
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPM2_A_KARRAS
                case "lms":
                    pretty_sampler_name = JHCivitaiSamplerEnum.LMS
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.LMS_KARRAS
                case "dpm_fast":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPM_FAST
                case "dpm_adaptive":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPM_ADAPTIVE
                case "dpmpp_2s_ancestral":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_2S_A
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_2S_A_KARRAS
                case "dpmpp_sde" | "dpmpp_sde_gpu":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_SDE
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_SDE_KARRAS
                case "dpmpp_2m":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_2M
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_2M_KARRAS
                case "dpmpp_2m_sde" | "dpmpp_2m_sde_gpu":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_2M_SDE
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_2M_SDE_KARRAS
                case "dpmpp_3m_sde" | "dpmpp_3m_sde_gpu":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_3M_SDE
                    if scheduler_name == "karras":
                        pretty_sampler_name = JHCivitaiSamplerEnum.DPMPP_3M_SDE_KARRAS
                    if scheduler_name == "exponential":
                        pretty_sampler_name = (
                            JHCivitaiSamplerEnum.DPMPP_3M_SDE_EXPONENTIAL
                        )
                case "lcm":
                    pretty_sampler_name = JHCivitaiSamplerEnum.LCM
                case "ddim":
                    pretty_sampler_name = JHCivitaiSamplerEnum.DDIM
                case "uni_pc" | "uni_pc_bh2":
                    pretty_sampler_name = JHCivitaiSamplerEnum.UNIPC

            last_line_parts.append(f"Sampler: {pretty_sampler_name}")

        if scheduler_name is not None:
            last_line_parts.append(f"Schedule type: {scheduler_name.capitalize()}")

        if cfg is not None:
            last_line_parts.append(f"CFG scale: {cfg}")

        if guidance is not None:
            last_line_parts.append(f"Distilled CFG Scale: {guidance}")

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
