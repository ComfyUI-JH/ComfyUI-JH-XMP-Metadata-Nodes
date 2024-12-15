import textwrap
from typing import Any, Dict, Final, Tuple


class JHFormatInstructionsNode:
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
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "format_string": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": cls.DEFAULT_FORMAT_STRING,
                        "placeholder": cls.DEFAULT_FORMAT_STRING,
                        "dynamicPrompts": False,
                    },
                ),
            },
            "optional": {
                "prompt": (("STRING"), {"defaultInput": True, "default": None}),
                "negative_prompt": (
                    ("STRING"),
                    {"defaultInput": True, "default": None},
                ),
                "model_name": (("STRING"), {"defaultInput": True, "default": None}),
                "seed": (("INT"), {"defaultInput": True, "default": None}),
                "sampler_name": (
                    ("STRING"),
                    {"defaultInput": True, "default": None},
                ),
                "scheduler_name": (
                    ("STRING"),
                    {"defaultInput": True, "default": None},
                ),
                "steps": ("INT", {"defaultInput": True, "default": None}),
                "cfg": (("FLOAT"), {"defaultInput": True, "default": None}),
                "guidance": (("FLOAT"), {"defaultInput": True, "default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_instructions"
    CATEGORY = "XMP Metadata Nodes"

    @classmethod
    def IS_CHANGED(cls, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
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
                f"Invalid placeholder '{exc.args[0]}' in format_string. "
                "Ensure all placeholders match the available keys: "
                "{prompt, negative_prompt, model_name, seed, sampler_name, "
                "scheduler_name, steps, cfg, guidance}."
            ) from exc

    def format_instructions(
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
    ) -> Tuple[str]:
        self.validate_format_string(format_string)
        formatted_string = format_string.format(
            prompt=prompt or "",
            negative_prompt=negative_prompt or "",
            model_name=model_name or "",
            sampler_name=sampler_name or "",
            scheduler_name=scheduler_name or "",
            steps="" if steps is None else steps,  # Ensure 0 is not treated as None
            seed=seed or "",
            cfg="" if cfg is None else cfg,  # Same for cfg
            guidance="" if guidance is None else guidance,
        )
        return (formatted_string,)
