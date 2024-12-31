import json
from enum import StrEnum
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import numpy as np
import piexif
import piexif.helper
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


JHImageSuffixForType: dict[JHSupportedImageTypes, str] = {
    JHSupportedImageTypes.JPEG: "jpeg",
    JHSupportedImageTypes.PNG_WITH_WORKFLOW: "png",
    JHSupportedImageTypes.PNG: "png",
    JHSupportedImageTypes.LOSSLESS_WEBP: "webp",
    JHSupportedImageTypes.WEBP: "webp",
}


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

        filename_extension = JHImageSuffixForType[image_type]

        batch_number: int = 0
        image: torch.Tensor

        for batch_number, image in enumerate(images):
            i: np.ndarray = 255.0 * image.cpu().numpy()
            img: Image = PIL.Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num: str = filename.replace(
                "%batch_num%", str(batch_number)
            )
            file: str = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            xml = ""
            if xml_string is not None:
                xml = xml_string
            else:
                xmpmetadata = JHXMPMetadata()
                # fmt: off
                xmpmetadata.creator = (
                    creator[batch_number]
                    if isinstance(creator, list)
                    else creator
                )
                xmpmetadata.rights = (
                    rights[batch_number]
                    if isinstance(rights, list)
                    else rights
                )
                xmpmetadata.title = (
                    title[batch_number]
                    if isinstance(title, list)
                    else title
                )
                xmpmetadata.description = (
                    description[batch_number]
                    if isinstance(description, list)
                    else description
                )
                xmpmetadata.subject = (
                    subject[batch_number]
                    if isinstance(subject, list)
                    else subject
                )
                xmpmetadata.instructions = (
                    instructions[batch_number]
                    if isinstance(instructions, list)
                    else instructions
                )
                if image_type == JHSupportedImageTypes.PNG_WITH_WORKFLOW or image_type == JHSupportedImageTypes.PNG:  # noqa: E501
                    xmpmetadata.comment = (
                        civitai_metadata[batch_number]
                        if isinstance(civitai_metadata, list)
                        else civitai_metadata
                    )
                xmpmetadata.alt_text = (
                    alt_text[batch_number]
                    if isinstance(alt_text, list)
                    else alt_text
                )
                xmpmetadata.ext_description = (
                    ext_description[batch_number]
                    if isinstance(ext_description, list)
                    else ext_description
                )
                # fmt: on
                xml = xmpmetadata.to_wrapped_string()

            self.save_image(
                img,
                image_type,
                Path(full_output_folder) / file,
                civitai_metadata,
                xml,
                prompt,
                extra_pnginfo,
            )

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"result": (images,), "ui": {"images": results}}

    def save_image(
        self,
        image: Image,
        image_type: JHSupportedImageTypes,
        to_path: Path,
        civitai_metadata: str | None = None,
        xml: str | None = None,
        prompt: str | None = None,
        extra_pnginfo: dict[str, Any] | None = None,
    ) -> None:
        match image_type:
            case JHSupportedImageTypes.PNG_WITH_WORKFLOW:
                pnginfo: PngInfo = PngInfo()

                if civitai_metadata is not None:
                    pnginfo.add_text("parameters", civitai_metadata)

                if xml is not None:
                    pnginfo.add_text("XML:com.adobe.xmp", xml)

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

                if xml is not None:
                    pnginfo.add_text("XML:com.adobe.xmp", xml)

                image.save(
                    to_path,
                    pnginfo=pnginfo,
                    compress_level=self.compress_level,
                )

            case JHSupportedImageTypes.JPEG:
                if xml is not None:
                    image.save(
                        to_path,
                        xmp=xml.encode("utf-8"),
                    )
                else:
                    image.save(to_path)

                if civitai_metadata is not None:
                    exif_bytes = piexif.dump(
                        {
                            "Exif": {
                                piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(  # noqa: E501
                                    civitai_metadata, encoding="unicode"
                                )
                            },
                        }
                    )
                    piexif.insert(exif_bytes, str(to_path))

            case JHSupportedImageTypes.LOSSLESS_WEBP:
                image.save(
                    to_path,
                    xmp=xml,
                    lossless=True,
                )

                if civitai_metadata is not None:
                    exif_bytes = piexif.dump(
                        {
                            "Exif": {
                                piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(  # noqa: E501
                                    civitai_metadata, encoding="unicode"
                                )
                            },
                        }
                    )
                    piexif.insert(exif_bytes, str(to_path))

            case JHSupportedImageTypes.WEBP:
                image.save(to_path, xmp=xml)

                if civitai_metadata is not None:
                    exif_bytes = piexif.dump(
                        {
                            "Exif": {
                                piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(  # noqa: E501
                                    civitai_metadata, encoding="unicode"
                                )
                            },
                        }
                    )
                    piexif.insert(exif_bytes, str(to_path))
