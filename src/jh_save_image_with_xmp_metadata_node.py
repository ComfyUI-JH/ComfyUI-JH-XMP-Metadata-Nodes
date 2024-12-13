import json
import os
from enum import StrEnum

import folder_paths
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from .jh_xmp_metadata import JHXMPMetadata


class JHSupportedImageTypes(StrEnum):
    JPEG = "JPEG"
    PNG_WITH_WORKFLOW = "PNG with embedded workflow"
    PNG = "PNG"
    LOSSLESS_WEBP = "Lossless WebP"
    WEBP = "WebP"


class JHSaveImageWithXMPMetadataNode:
    def __init__(self, output_dir: str | None = None):
        self.output_dir: str = (
            output_dir
            if output_dir is not None
            else folder_paths.get_output_directory()
        )
        self.type: str = "output"
        self.prefix_append: str = ""
        self.compress_level: int = 0

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
                        "default": JHSupportedImageTypes.PNG_WITH_WORKFLOW,
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
                "xml_string": (
                    "STRING",
                    {
                        "tooltip": (
                            "XMP metadata as an XML string. This will override all other fields."
                        ),
                        "forceInput": True,
                    },
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
        images: list,
        filename_prefix: str = "ComfyUI",
        image_type: JHSupportedImageTypes = JHSupportedImageTypes.PNG_WITH_WORKFLOW,
        creator: str | list | None = None,
        title: str | list | None = None,
        description: str | list | None = None,
        subject: str | list | None = None,
        instructions: str | list | None = None,
        xml_string: str | None = None,
        prompt: str | None = None,
        extra_pnginfo: dict | None = None,
    ) -> dict:
        if images is None or len(images) == 0:
            raise ValueError("No images to save.")

        filename_prefix += self.prefix_append
        full_output_folder: str
        filename: str
        counter: int
        subfolder: str
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        xmpmetadata: JHXMPMetadata | None = None
        results: list = []

        match image_type:
            case JHSupportedImageTypes.JPEG:
                filename_extension: str = "jpg"
            case JHSupportedImageTypes.PNG_WITH_WORKFLOW:
                filename_extension: str = "png"
            case JHSupportedImageTypes.PNG:
                filename_extension: str = "png"
            case JHSupportedImageTypes.LOSSLESS_WEBP:
                filename_extension: str = "webp"
            case JHSupportedImageTypes.WEBP:
                filename_extension: str = "webp"
            case _:
                raise ValueError(f"Unsupported image type: {image_type}")

        for batch_number, image in enumerate(images):
            i: np.ndarray = 255.0 * image.cpu().numpy()
            img: Image = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num: str = filename.replace("%batch_num%", str(batch_number))
            file: str = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            if xml_string is not None:
                xmp: str = xml_string
            else:
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
                xmp = xmpmetadata.to_wrapped_string().encode("utf-8")

            match image_type:
                case JHSupportedImageTypes.PNG_WITH_WORKFLOW:
                    pnginfo: PngInfo = PngInfo()
                    pnginfo.add_text("XML:com.adobe.xmp", xmp)
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
                    pnginfo: PngInfo = PngInfo()
                    pnginfo.add_text("XML:com.adobe.xmp", xmp)
                    img.save(
                        os.path.join(full_output_folder, file),
                        pnginfo=pnginfo,
                        compress_level=self.compress_level,
                    )

                case JHSupportedImageTypes.JPEG:
                    img.save(
                        os.path.join(full_output_folder, file),
                        xmp=xmp.encode("utf-8"),
                    )

                case JHSupportedImageTypes.LOSSLESS_WEBP:
                    img.save(
                        os.path.join(full_output_folder, file),
                        xmp=xmp,
                        lossless=True,
                    )

                case JHSupportedImageTypes.WEBP:
                    img.save(
                        os.path.join(full_output_folder, file),
                        xmp=xmp,
                    )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": (images,), "ui": {"images": results}}
