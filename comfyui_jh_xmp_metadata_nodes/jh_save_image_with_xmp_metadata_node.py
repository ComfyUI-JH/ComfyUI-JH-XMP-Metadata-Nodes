import json
from enum import StrEnum
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import numpy as np
import PIL.Image
import torch
from PIL.Image import Image
from PIL.PngImagePlugin import PngInfo

from comfyui_jh_xmp_metadata_nodes import jh_types

from .jh_xmp_metadata import JHXMPMetadata

try:
    import folder_paths  # pyright: ignore[reportMissingImports]
except ImportError:
    folder_paths = MagicMock()


class JHSupportedImageTypes(StrEnum):
    JPEG = "JPEG"
    PNG_WITH_WORKFLOW = "PNG with embedded workflow"
    PNG = "PNG"
    LOSSLESS_WEBP = "Lossless WebP"
    WEBP = "WebP"


class JHSaveImageWithXMPMetadataNode:
    def __init__(self, output_dir: str | None = None) -> None:
        self.output_dir: str = (
            output_dir
            if output_dir is not None
            else folder_paths.get_output_directory()
        )
        self.type: str = "output"
        self.prefix_append: str = ""
        self.compress_level: int = 0

    @classmethod
    def INPUT_TYPES(cls) -> jh_types.JHInputTypesType:
        # fmt: off
        return {
            "required": {
                "images": (
                    jh_types.JHNodeInputOutputTypeEnum.IMAGE, {
                        "tooltip": "The images to save."
                    }
                ),
                "filename_prefix": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "default": "ComfyUI",
                        "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",  # noqa: E501
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
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "dc:creator",
                        "forceInput": True
                    },
                ),
                "rights": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "dc:rights",
                        "forceInput": True
                    },
                ),
                "title": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "dc:title",
                        "forceInput": True
                    },
                ),
                "description": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "dc:description",
                        "forceInput": True
                    },
                ),
                "subject": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "dc:subject",
                        "forceInput": True
                },
                ),
                "instructions": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "photoshop:Instructions",
                        "forceInput": True
                    },
                ),
                "comment": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "exif:UserComment",
                        "forceInput": True
                    },
                ),
                "alt_text": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "Iptc4xmpCore:AltTextAccessibility",
                        "forceInput": True,
                    },
                ),
                "ext_description": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "Iptc4xmpCore:ExtDescrAccessibility",
                        "forceInput": True,
                    },
                ),
                "civitai_metadata": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "forceInput": True,
                    },
                ),
                "xml_string": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "tooltip": "XMP metadata as an XML string. This will override all other fields.",  # noqa: E501
                        "forceInput": True,
                    },
                ),
            },
            "hidden": {
                "prompt": jh_types.JHNodeInputOutputTypeEnum.PROMPT,
                "extra_pnginfo": jh_types.JHNodeInputOutputTypeEnum.EXTRA_PNGINFO,
            },
        }
        # fmt: on

    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.IMAGE,)
    FUNCTION = "save_images"
    CATEGORY = "XMP Metadata Nodes"
    OUTPUT_NODE = True

    def save_images(
        self,
        images: list,
        filename_prefix: str = "ComfyUI",
        image_type: JHSupportedImageTypes = JHSupportedImageTypes.PNG_WITH_WORKFLOW,
        creator: str | list | None = None,
        rights: str | list | None = None,
        title: str | list | None = None,
        description: str | list | None = None,
        subject: str | list | None = None,
        instructions: str | list | None = None,
        comment: str | list | None = None,
        alt_text: str | list | None = None,
        ext_description: str | list | None = None,
        civitai_metadata: str | None = None,
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

        batch_number: int = 0
        image: torch.Tensor

        for batch_number, image in enumerate(images):
            i: np.ndarray = 255.0 * image.cpu().numpy()
            img: Image = PIL.Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num: str = filename.replace(
                "%batch_num%", str(batch_number)
            )
            file: str = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            xmp = self.inputs_to_xml(
                creator,
                rights,
                title,
                description,
                subject,
                instructions,
                comment,
                alt_text,
                ext_description,
                xml_string,
                batch_number,
            )

            self.save_image(
                img,
                image_type,
                Path(full_output_folder) / file,
                civitai_metadata,
                xmp,
                prompt,
                extra_pnginfo,
            )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": (images,), "ui": {"images": results}}

    def get_batch_value(
        self, prop: str | list[str] | None, batch_number: int
    ) -> str | None:
        if isinstance(prop, list):
            return prop[batch_number]
        else:
            return prop

    def inputs_to_xml(
        self,
        creator: str | list[str] | None,
        rights: str | list[str] | None,
        title: str | list[str] | None,
        description: str | list[str] | None,
        subject: str | list[str] | None,
        instructions: str | list[str] | None,
        comment: str | list[str] | None,
        alt_text: str | list[str] | None,
        ext_description: str | list[str] | None,
        xml_string: str | None,
        batch_number: int,
    ) -> str:
        if xml_string is not None:
            xml: str = xml_string
        else:
            xmpmetadata = JHXMPMetadata()
            xmpmetadata.creator = self.get_batch_value(creator, batch_number)
            xmpmetadata.rights = self.get_batch_value(rights, batch_number)
            xmpmetadata.title = self.get_batch_value(title, batch_number)
            xmpmetadata.description = self.get_batch_value(description, batch_number)
            xmpmetadata.subject = self.get_batch_value(subject, batch_number)
            xmpmetadata.instructions = self.get_batch_value(instructions, batch_number)
            xmpmetadata.comment = self.get_batch_value(comment, batch_number)
            xmpmetadata.alt_text = self.get_batch_value(alt_text, batch_number)
            xmpmetadata.ext_description = self.get_batch_value(
                ext_description, batch_number
            )
            xml = xmpmetadata.to_wrapped_string()
        return xml

    def extension_for_type(self, image_type: JHSupportedImageTypes) -> str:
        filename_extension: str
        match image_type:
            case JHSupportedImageTypes.JPEG:
                filename_extension: str = "jpeg"
            case JHSupportedImageTypes.PNG_WITH_WORKFLOW:
                filename_extension: str = "png"
            case JHSupportedImageTypes.PNG:
                filename_extension: str = "png"
            case JHSupportedImageTypes.LOSSLESS_WEBP:
                filename_extension: str = "webp"
            case JHSupportedImageTypes.WEBP:
                filename_extension: str = "webp"
        return filename_extension

    def save_image(
        self,
        image: Image,
        image_type: JHSupportedImageTypes,
        to_path: Path,
        civitai_metadata: str | None = None,
        xmp: str | None = None,
        prompt: str | None = None,
        extra_pnginfo: dict[str, Any] | None = None,
    ) -> None:
        match image_type:
            case JHSupportedImageTypes.PNG_WITH_WORKFLOW:
                pnginfo: PngInfo = PngInfo()

                if civitai_metadata is not None:
                    pnginfo.add_text("parameters", civitai_metadata)

                if xmp is not None:
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

                if civitai_metadata is not None:
                    pnginfo.add_text("parameters", civitai_metadata)

                if xmp is not None:
                    pnginfo.add_text("XML:com.adobe.xmp", xmp)

                image.save(
                    to_path,
                    pnginfo=pnginfo,
                    compress_level=self.compress_level,
                )

            case JHSupportedImageTypes.JPEG:
                if xmp is not None:
                    image.save(
                        to_path,
                        xmp=xmp.encode("utf-8"),
                    )
                else:
                    image.save(to_path)

            case JHSupportedImageTypes.LOSSLESS_WEBP:
                image.save(
                    to_path,
                    xmp=xmp,
                    lossless=True,
                )

            case JHSupportedImageTypes.WEBP:
                image.save(to_path, xmp=xmp)
