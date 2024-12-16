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
        return {
            "required": {"image": (cls.get_image_files(), {"image_upload": True})},
        }

    @classmethod
    def get_image_files(cls) -> list[str]:
        input_dir: str = folder_paths.get_input_directory()
        files: list[str] = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        return sorted(files)

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
        # `image` here is a string, the name of the image file on disk;
        # just the filename, not the full path.
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
        width: int = 0
        height: int = 0

        excluded_formats = ["MPO"]

        for raw_frame in PIL.ImageSequence.Iterator(image_object):

            # Extract XMP metadata from the first frame, if available
            if len(output_images) == 0:
                xml_string = raw_frame.info.get("xmp", None)
                if isinstance(xml_string, bytes):
                    xml_string = xml_string.decode("utf-8")
                if xml_string:  # Ensure xml_string is not None or empty
                    xmp_metadata = JHXMPMetadata.from_string(xml_string)
                    creator = xmp_metadata.creator
                    title = xmp_metadata.title
                    description = xmp_metadata.description
                    subject = xmp_metadata.subject
                    instructions = xmp_metadata.instructions

            # Fix image orientation based on EXIF metadata. Do this in
            # place to avoid creating a new image object for each frame.
            PIL.ImageOps.exif_transpose(raw_frame, in_place=True)

            # Convert 32-bit integer images to RGB
            if raw_frame.mode == "I":
                raw_frame = raw_frame.point(lambda i: i * (1 / 255))
            rgb_frame = raw_frame.convert("RGB")

            # Ensure all frames are the same size as the first frame
            if len(output_images) == 0:
                width = rgb_frame.size[0]
                height = rgb_frame.size[1]
            if rgb_frame.size[0] != width or rgb_frame.size[1] != height:
                continue

            # Normalize the image to a tensor with values in [0, 1]
            np_array = np.array(rgb_frame).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(np_array)[None,]

            # Go back to the original multichannel(?) frame and extract
            # the alpha channel as a mask
            if "A" in raw_frame.getbands():
                np_array = (
                    np.array(raw_frame.getchannel("A")).astype(np.float32) / 255.0
                )
                mask_tensor = 1.0 - torch.from_numpy(np_array)
            else:
                mask_tensor = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            # Append the processed image and mask to the outputs
            output_images.append(image_tensor)
            output_masks.append(mask_tensor.unsqueeze(0))

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
