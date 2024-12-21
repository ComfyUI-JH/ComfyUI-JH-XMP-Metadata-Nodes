import textwrap
from typing import Any, Final

from comfyui_jh_xmp_metadata_nodes import jh_types


class JHFormatMetadataNode:
    DEFAULT_FORMAT_STRING: Final[str] = textwrap.dedent(
        """
        Prompt: {prompt}
        Negative Prompt: {negative_prompt}
        Model: {model_name}
        Seed: {seed}
        Sampler: {sampler_name}
        Scheduler: {scheduler_name}
        Steps: {steps}
        CFG: {cfg}
        Guidance: {guidance}
        """
    ).strip()

    @classmethod
    def INPUT_TYPES(cls) -> jh_types.JHInputTypesType:
        # fmt: off
        return {
            "required": {
                "format_string": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "multiline": True,
                        "default": cls.DEFAULT_FORMAT_STRING,
                        "placeholder": cls.DEFAULT_FORMAT_STRING,
                        "dynamicPrompts": False,
                    },
                ),
            },
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
                "model_name": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "defaultInput": True
                    }
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
            },
        }
        # fmt: on

    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.STRING,)
    FUNCTION = "format_metadata"
    CATEGORY = "XMP Metadata Nodes"

    @classmethod
    def IS_CHANGED(
        cls,  # pylint: disable=unused-argument
        *args: tuple[Any],
        **kwargs: dict[str, Any],
    ) -> bool:
        return True

    @staticmethod
    def validate_format_string(format_string: str) -> None:
        try:
            format_string.format(
                prompt="",
                negative_prompt="",
                model_name="",
                sampler_name="",
                scheduler_name="",
                steps="",
                seed="",
                cfg="",
                guidance="",
            )
        except KeyError as exc:
            raise ValueError(
                f"Invalid placeholder '{exc.args[0]}' in format_string."
            ) from exc

    def format_metadata(
        self,
        prompt: str | None = None,
        negative_prompt: str | None = None,
        model_name: str | None = None,
        seed: int | None = None,
        sampler_name: str | None = None,
        scheduler_name: str | None = None,
        steps: int | None = None,
        cfg: float | None = None,
        guidance: float | None = None,
        format_string: str = DEFAULT_FORMAT_STRING,
    ) -> tuple[str]:
        self.validate_format_string(format_string)
        formatted_string = format_string.format(
            prompt=prompt or "",
            negative_prompt=negative_prompt or "",
            model_name=model_name or "",
            sampler_name=sampler_name or "",
            scheduler_name=scheduler_name or "",
            steps="" if steps is None else steps,  # Ensure 0 is not treated as None
            seed="" if seed is None else seed,  # Ensure 0 is treated as a valid value
            cfg="" if cfg is None else cfg,  # Same for cfg
            guidance="" if guidance is None else guidance,
        )
        return (formatted_string,)
