import textwrap
from typing import Final


class JHFormatInstructionsNode:
    DEFAULT_FORMAT_STRING: Final = textwrap.dedent(
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
    def INPUT_TYPES(cls):
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
    def IS_CHANGED(cls, **kwargs):
        return True

    def format_instructions(
        self,
        prompt=None,
        negative_prompt=None,
        model_name=None,
        seed=None,
        sampler_name=None,
        scheduler_name=None,
        steps=None,
        cfg=None,
        guidance=None,
        format_string=DEFAULT_FORMAT_STRING,
    ):
        formatted_string = format_string.format(
            prompt=prompt or "",
            negative_prompt=negative_prompt or "",
            model_name=model_name or "",
            sampler_name=sampler_name or "",
            scheduler_name=scheduler_name or "",
            steps=steps or "",
            seed=seed or "",
            cfg=cfg or "",
            guidance=guidance or "",
        )
        return (formatted_string,)
