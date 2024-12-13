import pytest
import os
import torch
from PIL import Image
from src.jh_save_image_with_xmp_metadata_node import (
    JHSupportedImageTypes,
    JHSaveImageWithXMPMetadataNode,
)
from src.jh_xmp_metadata import JHXMPMetadata


def test_JHSaveImageWithXMPMetadataNode_save_images_valid_input(tmp_path):
    node = JHSaveImageWithXMPMetadataNode(output_dir=str(tmp_path))
    images = torch.rand(2, 128, 128, 3)
    filename_prefix = "test_image"
    image_type = JHSupportedImageTypes.PNGWF
    creator = "John Doe, Jane Doe"
    title = "Test Title"
    description = "Test Description"
    subject = "Subject 1, Subject 2"
    instructions = "Test Instructions"
    prompt = "Test Prompt"
    extra_pnginfo = {"workflow": "value"}

    return_value = node.save_images(
        images,
        filename_prefix,
        image_type,
        creator,
        title,
        description,
        subject,
        instructions,
        prompt,
        extra_pnginfo,
    )

    # Check that the images were saved
    for image in return_value["ui"]["images"]:
        image_path = tmp_path / image["filename"]
        assert os.path.exists(image_path)

        # Check that the XMP metadata was saved
        image = Image.open(image_path)
        xml_string = image.info.get("xmp", "")
        xmp_metadata = JHXMPMetadata.from_string(xml_string)
        assert xmp_metadata.creator == creator
        assert xmp_metadata.title == title
        assert xmp_metadata.description == description
        assert xmp_metadata.subject == subject
        assert xmp_metadata.instructions == instructions


def test_JHSaveImageWithXMPMetadataNode_save_images_invalid_image_type():
    node = JHSaveImageWithXMPMetadataNode()
    images = torch.rand(2, 128, 128, 3)
    filename_prefix = "test_image"
    image_type = "Invalid Image Type"
    creator = "John Doe, Jane Doe"
    title = "Test Title"
    description = "Test Description"
    subject = "Subject 1, Subject 2"
    instructions = "Test Instructions"
    prompt = "Test Prompt"
    extra_pnginfo = {"key": "value"}

    with pytest.raises(ValueError):
        node.save_images(
            images,
            filename_prefix,
            image_type,
            creator,
            title,
            description,
            subject,
            instructions,
            prompt,
            extra_pnginfo,
        )


def test_JHSaveImageWithXMPMetadataNode_save_images_empty_images():
    node = JHSaveImageWithXMPMetadataNode()
    images = []
    filename_prefix = "test_image"
    image_type = JHSupportedImageTypes.PNGWF
    creator = "John Doe, Jane Doe"
    title = "Test Title"
    description = "Test Description"
    subject = "Subject 1, Subject 2"
    instructions = "Test Instructions"
    prompt = "Test Prompt"
    extra_pnginfo = {"key": "value"}

    with pytest.raises(ValueError):
        node.save_images(
            images,
            filename_prefix,
            image_type,
            creator,
            title,
            description,
            subject,
            instructions,
            prompt,
            extra_pnginfo,
        )
