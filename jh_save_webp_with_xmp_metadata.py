from enum import Enum
import os

import json
import numpy as np
from PIL import Image, ExifTags
from PIL.PngImagePlugin import PngInfo

import folder_paths

from .jh_xmp_metadata import JHXMPMetadata


class JHSaveWebPWithXMPMetadata:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "ComfyUI",
                        "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",
                    },
                ),
                "lossless": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING",),
                "subject": ("STRING",),
                "title": ("STRING",),
                "instructions": ("STRING",),
                "make": ("STRING", {"default": "ComfyUI"}),
                "model": ("STRING",),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "save_images"
    CATEGORY = "JHXMP"
    OUTPUT_NODE = True

    def save_images(
        self,
        images,
        filename_prefix="ComfyUI",
        lossless=True,
        description=None,
        subject=None,
        title=None,
        instructions=None,
        make=None,
        model=None,
        prompt=None,
        extra_pnginfo=None,
    ):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        filename_extension = "webp"
        results = list()

        xmpmetadata = JHXMPMetadata()
        xmpmetadata.title = title
        xmpmetadata.description = description
        xmpmetadata.subject = subject
        xmpmetadata.instructions = instructions
        xmpmetadata.make = make
        xmpmetadata.model = model

        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            img.save(
                os.path.join(full_output_folder, file),
                xmp=xmpmetadata.to_wrapped_string(),
                lossless=lossless,
            )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": images, "ui": {"images": results}}
