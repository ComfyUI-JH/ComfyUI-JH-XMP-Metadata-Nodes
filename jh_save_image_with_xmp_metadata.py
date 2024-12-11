from enum import Enum
import os

import json
import numpy as np
from PIL import Image, ExifTags
from PIL.PngImagePlugin import PngInfo

import folder_paths

from .jh_xmp_metadata import JHXMPMetadata


class JHSupportedImageTypes(Enum):
    PNG = "PNG"
    WEBP = "WebP"


class JHSaveImageWithXMPMetadata:
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
                "image_type": (
                    [x.value for x in JHSupportedImageTypes],
                    {
                        "default": JHSupportedImageTypes.PNG.value,
                    },
                ),
                "embed_workflow": ("BOOLEAN", {"default": True}),
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
    CATEGORY = "XMP Metadata Nodes"
    OUTPUT_NODE = True

    def save_images(
        self,
        images,
        filename_prefix="ComfyUI",
        image_type=JHSupportedImageTypes.PNG.value,
        embed_workflow=True,
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
        results = list()

        match image_type:
            case JHSupportedImageTypes.PNG.value:
                filename_extension = "png"
            case JHSupportedImageTypes.WEBP.value:
                filename_extension = "webp"

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

            match image_type:
                case JHSupportedImageTypes.PNG.value:
                    pnginfo = PngInfo()
                    pnginfo.add_text(
                        "XML:com.adobe.xmp", xmpmetadata.to_wrapped_string()
                    )

                    if embed_workflow:
                        if prompt is not None:
                            pnginfo.add_text("prompt", json.dumps(prompt))
                        if extra_pnginfo is not None:
                            pnginfo.add_text(
                                "workflow", json.dumps(extra_pnginfo["workflow"])
                            )

                    img.save(
                        os.path.join(full_output_folder, file),
                        pnginfo=pnginfo,
                        compress_level=self.compress_level,
                    )

                case JHSupportedImageTypes.WEBP.value:
                    if embed_workflow:
                        exif_dict = {}
                        if prompt is not None:
                            exif_dict["prompt"] = json.dumps(prompt)
                        if extra_pnginfo is not None:
                            exif_dict.update(extra_pnginfo)

                        exif = img.getexif()
                        exif_addr = ExifTags.Base.UserComment
                        for key in exif_dict:
                            exif[exif_addr] = "{}:{}".format(
                                key, json.dumps(exif_dict[key])
                            )
                            exif_addr -= 1

                    img.save(
                        os.path.join(full_output_folder, file),
                        exif=exif,
                        xmp=xmpmetadata.to_wrapped_string(),
                        quality=100,
                        lossless=True,
                    )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": images, "ui": {"images": results}}
