import json
from enum import StrEnum
from pathlib import Path

import folder_paths  # pyright: ignore[reportMissingImports]; pylint: disable=import-error
import numpy as np
import PIL.Image
from PIL.Image import Image
from PIL.PngImagePlugin import PngInfo

from .jh_xmp_metadata import JHXMPMetadata


class JHSupportedImageTypes(StrEnum):
    INVALID_TYPE = "INVALID_TYPE"
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
        results: list = []

        filename_extension: str = self.extension_for_type(image_type)

        for batch_number, image in enumerate(images):
            i: np.ndarray = 255.0 * image.cpu().numpy()
            img: Image = PIL.Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num: str = filename.replace(
                "%batch_num%", str(batch_number)
            )
            file: str = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            xmp = self.xmp(
                creator,
                title,
                description,
                subject,
                instructions,
                xml_string,
                batch_number,
            )

            self.save_image(
                img,
                image_type,
                Path(full_output_folder) / file,
                xmp,
                prompt,
                extra_pnginfo,
            )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": (images,), "ui": {"images": results}}

    def xmp(
        self,
        creator,
        title,
        description,
        subject,
        instructions,
        xml_string,
        batch_number,
    ) -> str:
        xmp: str
        if xml_string is not None:
            xmp = xml_string
        else:
            xmpmetadata = JHXMPMetadata()
            xmpmetadata.creator = (
                creator[batch_number] if isinstance(creator, list) else creator
            )
            xmpmetadata.title = (
                title[batch_number] if isinstance(title, list) else title
            )
            xmpmetadata.description = (
                description[batch_number]
                if isinstance(description, list)
                else description
            )
            xmpmetadata.subject = (
                subject[batch_number] if isinstance(subject, list) else subject
            )
            xmpmetadata.instructions = (
                instructions[batch_number]
                if isinstance(instructions, list)
                else instructions
            )
            xmp = xmpmetadata.to_wrapped_string()
        return xmp

    def extension_for_type(self, image_type: JHSupportedImageTypes) -> str:

        filename_extension: str
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
        return filename_extension

    def save_image(
        self,
        image: Image,
        image_type: JHSupportedImageTypes,
        to_path: Path,
        xmp: str,
        prompt: str | None = None,
        extra_pnginfo: dict | None = None,
    ) -> None:

        match image_type:
            case JHSupportedImageTypes.PNG_WITH_WORKFLOW:
                pnginfo: PngInfo = PngInfo()
                pnginfo.add_text("XML:com.adobe.xmp", xmp)
                if prompt is not None:
                    pnginfo.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    pnginfo.add_text("workflow", json.dumps(extra_pnginfo["workflow"]))
                image.save(
                    to_path,
                    pnginfo=pnginfo,
                    compress_level=self.compress_level,
                )

            case JHSupportedImageTypes.PNG:
                pnginfo: PngInfo = PngInfo()
                pnginfo.add_text("XML:com.adobe.xmp", xmp)
                image.save(
                    to_path,
                    pnginfo=pnginfo,
                    compress_level=self.compress_level,
                )

            case JHSupportedImageTypes.JPEG:
                image.save(
                    to_path,
                    xmp=xmp.encode("utf-8"),
                )

            case JHSupportedImageTypes.LOSSLESS_WEBP:
                image.save(
                    to_path,
                    xmp=xmp,
                    lossless=True,
                )

            case JHSupportedImageTypes.WEBP:
                image.save(to_path, xmp=xmp)

            case _:
                raise ValueError(f"Unsupported image type: {image_type}")
