import textwrap
from typing import Any, Dict, Final, Tuple


class JHFormatInstructionsNode:
    """
    A utility class for formatting metadata into a structured string based on
    customizable templates. This class provides a default format string and
    allows users to supply custom templates with placeholders for specific
    metadata fields.
    """

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
    def INPUT_TYPES(cls) -> Dict[str, Any]:  # pylint: disable=invalid-name
        """
        Defines the input types for the format instructions node.

        Returns:
            A dictionary containing required and optional inputs with their
            respective types and defaults.
        """
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
    def IS_CHANGED(cls, **kwargs: Any) -> bool:  # pylint: disable=unused-argument,invalid-name
        """
        Determines if the node has changed based on the provided arguments.

        Args:
            kwargs: Arbitrary keyword arguments representing node attributes.

        Returns:
            True, indicating the node always reports as changed.
        """
        return True

    @staticmethod
    def validate_format_string(format_string: str) -> None:
        """
        Validates the format string to ensure it contains only supported
        placeholders.

        Args:
            format_string: The format string to validate.

        Raises:
            ValueError: If the format string contains invalid placeholders.
        """
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
        prompt: str = None,
        negative_prompt: str = None,
        model_name: str = None,
        seed: int = None,
        sampler_name: str = None,
        scheduler_name: str = None,
        steps: int = None,
        cfg: float = None,
        guidance: float = None,
        format_string: str = DEFAULT_FORMAT_STRING,
    ) -> Tuple[str]:
        """
        Formats the input metadata into a structured string based on a template.

        Args:
            prompt: The prompt text.
            negative_prompt: The negative prompt text.
            model_name: The name of the model.
            seed: The random seed used.
            sampler_name: The name of the sampler.
            scheduler_name: The name of the scheduler.
            steps: The number of steps.
            cfg: The classifier-free guidance scale.
            guidance: The guidance scale.
            format_string: The format string template.

        Returns:
            A tuple containing the formatted string.

        Raises:
            ValueError: If the format_string contains invalid placeholders.
        """
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
