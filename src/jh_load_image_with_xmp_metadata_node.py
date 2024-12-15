import hashlib
import os

import folder_paths  # pyright: ignore[reportMissingImports]; pylint: disable=import-error
import numpy as np
import PIL.Image
import PIL.ImageOps
import PIL.ImageSequence
import torch

from .jh_xmp_metadata import JHXMPMetadata


class JHLoadImageWithXMPMetadataNode:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        return {
            "required": {"image": (sorted(files), {"image_upload": True})},
        }

    RETURN_TYPES = (
        "IMAGE",
        "MASK",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "IMAGE",
        "MASK",
        "creator",
        "title",
        "description",
        "subject",
        "instructions",
        "xml_string",
    )
    FUNCTION = "load_image"
    CATEGORY = "XMP Metadata Nodes"
    OUTPUT_NODE = False

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)

        creator = None
        title = None
        description = None
        subject = None
        instructions = None
        xml_string = None

        image_object = PIL.Image.open(image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ["MPO"]

        for i in PIL.ImageSequence.Iterator(image_object):

            # Extract XMP metadata from the first frame, if available
            if len(output_images) == 0:
                xml_string = i.info.get("xmp", None)
                if isinstance(xml_string, bytes):
                    xml_string = xml_string.decode("utf-8")
                if xml_string:  # Ensure xml_string is not None or empty
                    xmp_metadata = JHXMPMetadata.from_string(xml_string)
                    creator = xmp_metadata.creator
                    title = xmp_metadata.title
                    description = xmp_metadata.description
                    subject = xmp_metadata.subject
                    instructions = xmp_metadata.instructions

            # Fix image orientation based on EXIF metadata
            i = PIL.ImageOps.exif_transpose(i)

            # Convert 32-bit integer images to RGB
            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            # Ensure all frames are the same size as the first frame
            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]
            if image.size[0] != w or image.size[1] != h:
                continue

            # Normalize the image to a tensor with values in [0, 1]
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            # Generate the mask if the frame has an alpha channel, otherwise use an empty mask
            if "A" in i.getbands():
                mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            # Append the processed image and mask to the outputs
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        # Combine frames into a single tensor if multiple frames exist
        if len(output_images) > 1 and image_object.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return (
            output_image,
            output_mask,
            creator,
            title,
            description,
            subject,
            instructions,
            xml_string,
        )

    @classmethod
    def IS_CHANGED(cls, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image):
        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
        return True
