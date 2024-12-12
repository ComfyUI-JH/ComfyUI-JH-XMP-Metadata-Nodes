from enum import StrEnum
import os

import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import folder_paths

from .jh_xmp_metadata import JHXMPMetadata


class JHSupportedImageTypes(StrEnum):
    JPEG = "JPEG"
    PNGWF = "PNG with embedded workflow"
    PNG = "PNG"
    WEBPL = "Lossless WebP"
    WEBP = "WebP"


class JHSaveImageWithXMPMetadataNode:
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
                        "tooltip": (
                            "The prefix for the file to save. This may include formatting "
                            "information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% "
                            "to include values from nodes."
                        ),
                    },
                ),
                "image_type": (
                    [x for x in JHSupportedImageTypes],
                    {
                        "default": JHSupportedImageTypes.PNGWF,
                    },
                ),
            },
            "optional": {
                "creator": (
                    "STRING",
                    {"tooltip": ("dc:creator"), "forceInput": True},
                ),
                "title": (
                    "STRING",
                    {"tooltip": ("dc:title"), "forceInput": True},
                ),
                "description": (
                    "STRING",
                    {"tooltip": ("dc:description"), "forceInput": True},
                ),
                "subject": (
                    "STRING",
                    {"tooltip": ("dc:subject"), "forceInput": True},
                ),
                "instructions": (
                    "STRING",
                    {"tooltip": ("photoshop:Instructions"), "forceInput": True},
                ),
                "make": (
                    "STRING",
                    {"tooltip": ("tiff:Make"), "forceInput": True},
                ),
                "model": (
                    "STRING",
                    {"tooltip": ("tiff:Model"), "forceInput": True},
                ),
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
        image_type=JHSupportedImageTypes.PNGWF,
        creator=None,
        title=None,
        description=None,
        subject=None,
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
        filename_extension = "png"
        results = list()

        match image_type:
            case JHSupportedImageTypes.JPEG:
                filename_extension = "jpg"
            case JHSupportedImageTypes.PNGWF:
                filename_extension = "png"
            case JHSupportedImageTypes.PNG:
                filename_extension = "png"
            case JHSupportedImageTypes.WEBPL:
                filename_extension = "webp"
            case JHSupportedImageTypes.WEBP:
                filename_extension = "webp"

        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            xmpmetadata = JHXMPMetadata()

            if isinstance(creator, list):
                xmpmetadata.creator = creator[batch_number]
            else:
                xmpmetadata.creator = creator

            if isinstance(title, list):
                xmpmetadata.title = title[batch_number]
            else:
                xmpmetadata.title = title

            if isinstance(description, list):
                xmpmetadata.description = description[batch_number]
            else:
                xmpmetadata.description = description

            if isinstance(subject, list):
                xmpmetadata.subject = subject[batch_number]
            else:
                xmpmetadata.subject = subject

            if isinstance(instructions, list):
                xmpmetadata.instructions = instructions[batch_number]
            else:
                xmpmetadata.instructions = instructions

            if isinstance(make, list):
                xmpmetadata.make = make[batch_number]
            else:
                xmpmetadata.make = make

            if isinstance(model, list):
                xmpmetadata.model = model[batch_number]
            else:
                xmpmetadata.model = model

            match image_type:
                case JHSupportedImageTypes.PNGWF:
                    pnginfo = PngInfo()
                    pnginfo.add_text(
                        "XML:com.adobe.xmp", xmpmetadata.to_wrapped_string()
                    )
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

                case JHSupportedImageTypes.PNG:
                    pnginfo = PngInfo()
                    pnginfo.add_text(
                        "XML:com.adobe.xmp", xmpmetadata.to_wrapped_string()
                    )
                    img.save(
                        os.path.join(full_output_folder, file),
                        pnginfo=pnginfo,
                        compress_level=self.compress_level,
                    )

                case JHSupportedImageTypes.JPEG:
                    img.save(
                        os.path.join(full_output_folder, file),
                        xmp=xmpmetadata.to_wrapped_string().encode("utf-8"),
                    )

                case JHSupportedImageTypes.WEBPL:
                    img.save(
                        os.path.join(full_output_folder, file),
                        xmp=xmpmetadata.to_wrapped_string(),
                        lossless=True,
                    )

                case JHSupportedImageTypes.WEBP:
                    img.save(
                        os.path.join(full_output_folder, file),
                        xmp=xmpmetadata.to_wrapped_string(),
                    )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": (images,), "ui": {"images": results}}
