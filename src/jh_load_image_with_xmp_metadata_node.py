import hashlib
import os

import folder_paths
import numpy as np
import torch
from PIL import Image, ImageOps, ImageSequence

from .jh_xmp_metadata import JHXMPMetadata


class JHLoadImageWithXMPMetadataNode:
    """
    A class representing a custom node to load images with embedded XMP metadata.

    This node provides functionality for loading images, extracting their XMP metadata,
    and converting them into a format suitable for processing, including generating
    image masks. It can handle multi-frame images and ensure consistent dimensions
    across loaded frames.

    This code was partially taken from ComfyUI, which is licensed under the GNU
    GPL v3 license. Used by permission. https://github.com/comfyanonymous/ComfyUI

    Attributes:
        INPUT_TYPES (dict): Defines the input types for the node, specifying the
            directory to fetch images and the required inputs.
        RETURN_TYPES (tuple): Specifies the types of outputs returned by the node,
            including the image, mask, and XMP metadata fields.
        RETURN_NAMES (tuple): Defines the names of the returned outputs for clarity
            and easy referencing.
        FUNCTION (str): The name of the function to invoke for processing the inputs.
        CATEGORY (str): Specifies the category under which this node is grouped.
        OUTPUT_NODE (bool): Indicates whether this node is an output node.

    Methods:
        INPUT_TYPES():
            Defines the input schema for the node, dynamically fetching available
            images from the input directory.

        load_image(image):
            Loads an image, processes it into a tensor, extracts its metadata if
            present, and generates a corresponding mask. Handles multi-frame images
            and ensures consistent dimensions across frames.

        IS_CHANGED(image):
            Generates a SHA-256 hash for the specified image file to check if the
            image has changed.

        VALIDATE_INPUTS(image):
            Validates the input image file by checking if the annotated file path
            exists.

    Dependencies:
        - Uses `Pillow` (PIL) for image handling and metadata extraction.
        - Uses `numpy` and `torch` for numerical operations and tensor manipulation.
        - Relies on `folder_paths` for managing input file paths and annotations.
        - Integrates with `JHXMPMetadata` for parsing and handling XMP metadata.

    Example Usage:
        # Instantiate and use the node
        node = JHLoadImageWithXMPMetadataNode()
        inputs = node.INPUT_TYPES()
        result = node.load_image("example_image.jpg")
        print(result)  # Outputs image, mask, and metadata fields.
    """
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        return {
            "required": {"image": (sorted(files), {"image_upload": True})},
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
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

        image_object = Image.open(image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ["MPO"]

        for i in ImageSequence.Iterator(image_object):

            # Extract XMP metadata from the first frame, if available
            if len(output_images) == 0:
                xml_string = i.info.get("xmp", None)
                if isinstance(xml_string, bytes):
                    xml_string = xml_string.decode("utf-8")
                if xml_string is not None:
                    xmp_metadata = JHXMPMetadata.from_string(xml_string)
                    creator = xmp_metadata.creator
                    title = xmp_metadata.title
                    description = xmp_metadata.description
                    subject = xmp_metadata.subject
                    instructions = xmp_metadata.instructions

            # Fix image orientation based on EXIF metadata
            i = ImageOps.exif_transpose(i)

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
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True
