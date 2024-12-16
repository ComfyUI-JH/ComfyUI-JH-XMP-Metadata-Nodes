from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import torch
from PIL import Image

from src.jh_save_image_with_xmp_metadata_node import (
    JHSaveImageWithXMPMetadataNode,
    JHSupportedImageTypes,
)

# pylint: disable=redefined-outer-name


@pytest.fixture
def mock_folder_paths():
    with patch("src.jh_save_image_with_xmp_metadata_node.folder_paths") as mock:
        yield mock


@pytest.fixture
def mock_image():
    return torch.rand(100, 100, 3)  # Generate a random PyTorch tensor


@pytest.fixture
def node(mock_folder_paths):
    mock_folder_paths.get_output_directory.return_value = "/mock/output/dir"
    mock_folder_paths.get_save_image_path.return_value = (
        "/mock/output/dir",
        "mock_filename",
        0,
        "mock_subfolder",
        "mock_filename_prefix",
    )
    return JHSaveImageWithXMPMetadataNode()


def test_save_images_no_images(node):
    with pytest.raises(ValueError, match="No images to save."):
        node.save_images([])


def test_save_images_jpeg(node, mock_image, mock_folder_paths):
    images = [mock_image]
    mock_save_image = MagicMock()
    node.save_image = mock_save_image

    result = node.save_images(images, image_type=JHSupportedImageTypes.JPEG)

    assert len(result["ui"]["images"]) == 1
    assert result["ui"]["images"][0]["filename"].endswith(".jpg")
    mock_save_image.assert_called_once()


def test_save_images_png_with_workflow(node, mock_image, mock_folder_paths):
    images = [mock_image]
    mock_save_image = MagicMock()
    node.save_image = mock_save_image

    result = node.save_images(
        images, image_type=JHSupportedImageTypes.PNG_WITH_WORKFLOW
    )

    assert len(result["ui"]["images"]) == 1
    assert result["ui"]["images"][0]["filename"].endswith(".png")
    mock_save_image.assert_called_once()


def test_save_images_with_metadata(node, mock_image, mock_folder_paths):
    images = [mock_image]
    mock_save_image = MagicMock()
    node.save_image = mock_save_image

    result = node.save_images(
        images,
        image_type=JHSupportedImageTypes.PNG,
        creator="Test Creator",
        title="Test Title",
        description="Test Description",
    )

    assert len(result["ui"]["images"]) == 1
    assert result["ui"]["images"][0]["filename"].endswith(".png")
    mock_save_image.assert_called_once()


def test_extension_for_type(node):
    assert node.extension_for_type(JHSupportedImageTypes.JPEG) == "jpg"
    assert node.extension_for_type(JHSupportedImageTypes.PNG) == "png"
    assert node.extension_for_type(JHSupportedImageTypes.LOSSLESS_WEBP) == "webp"
    assert node.extension_for_type(JHSupportedImageTypes.WEBP) == "webp"
    assert node.extension_for_type(JHSupportedImageTypes.PNG_WITH_WORKFLOW) == "png"


def test_extension_for_unsupported_type(node):
    with pytest.raises(ValueError, match="Unsupported image type"):
        node.extension_for_type("unsupported_type")


def test_xmp_with_xml_string(node):
    xml_string = "<xmpmeta>Test XML</xmpmeta>"
    result = node.xmp(
        creator=None,
        title=None,
        description=None,
        subject=None,
        instructions=None,
        xml_string=xml_string,
        batch_number=0,
    )
    assert result == xml_string


def test_xmp_with_metadata_fields(node):
    result = node.xmp(
        creator="Test Creator",
        title="Test Title",
        description="Test Description",
        subject="Test Subject",
        instructions="Test Instructions",
        xml_string=None,
        batch_number=0,
    )
    assert "Test Creator" in result
    assert "Test Title" in result
    assert "Test Description" in result
    assert "Test Subject" in result
    assert "Test Instructions" in result


def test_xmp_with_list_metadata_fields(node):
    result = node.xmp(
        creator=["Creator 1", "Creator 2"],
        title=["Title 1", "Title 2"],
        description=["Description 1", "Description 2"],
        subject=["Subject 1", "Subject 2"],
        instructions=["Instructions 1", "Instructions 2"],
        xml_string=None,
        batch_number=1,
    )
    assert "Creator 2" in result
    assert "Title 2" in result
    assert "Description 2" in result
    assert "Subject 2" in result
    assert "Instructions 2" in result


def test_save_image_jpeg(node, mock_image, tmp_path):
    img = Image.fromarray((mock_image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / "test_image.jpg"
    xmp = "<xmpmeta>Test XML</xmpmeta>"

    node.save_image(img, JHSupportedImageTypes.JPEG, to_path, xmp)

    assert to_path.exists()
    assert to_path.suffix == ".jpg"


def test_save_image_png_with_workflow(node, mock_image, tmp_path):
    img = Image.fromarray((mock_image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / "test_image.png"
    xmp = "<xmpmeta>Test XML</xmpmeta>"
    prompt = "Test Prompt"
    extra_pnginfo = {"workflow": "Test Workflow"}

    node.save_image(
        img,
        JHSupportedImageTypes.PNG_WITH_WORKFLOW,
        to_path,
        xmp,
        prompt,
        extra_pnginfo,
    )

    assert to_path.exists()
    assert to_path.suffix == ".png"


def test_save_image_png(node, mock_image, tmp_path):
    img = Image.fromarray((mock_image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / "test_image.png"
    xmp = "<xmpmeta>Test XML</xmpmeta>"

    node.save_image(img, JHSupportedImageTypes.PNG, to_path, xmp)

    assert to_path.exists()
    assert to_path.suffix == ".png"


def test_save_image_lossless_webp(node, mock_image, tmp_path):
    img = Image.fromarray((mock_image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / "test_image.webp"
    xmp = "<xmpmeta>Test XML</xmpmeta>"

    node.save_image(img, JHSupportedImageTypes.LOSSLESS_WEBP, to_path, xmp)

    assert to_path.exists()
    assert to_path.suffix == ".webp"


def test_save_image_webp(node, mock_image, tmp_path):
    img = Image.fromarray((mock_image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / "test_image.webp"
    xmp = "<xmpmeta>Test XML</xmpmeta>"

    node.save_image(img, JHSupportedImageTypes.WEBP, to_path, xmp)

    assert to_path.exists()
    assert to_path.suffix == ".webp"


def test_save_image_unsupported_type(node, mock_image, tmp_path):
    img = Image.fromarray((mock_image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / "test_image.unsupported"
    xmp = "<xmpmeta>Test XML</xmpmeta>"

    with pytest.raises(ValueError, match="Unsupported image type"):
        node.save_image(img, "unsupported_type", to_path, xmp)


def test_input_types(node):
    input_types = node.INPUT_TYPES()

    assert isinstance(input_types, dict)
    assert "required" in input_types
    assert "optional" in input_types
    assert "hidden" in input_types

    required_inputs = input_types["required"]
    optional_inputs = input_types["optional"]
    hidden_inputs = input_types["hidden"]

    assert isinstance(required_inputs, dict)
    assert isinstance(optional_inputs, dict)
    assert isinstance(hidden_inputs, dict)

    # Check required inputs
    assert "images" in required_inputs
    assert "filename_prefix" in required_inputs
    assert "image_type" in required_inputs

    # Check optional inputs
    assert "creator" in optional_inputs
    assert "title" in optional_inputs
    assert "description" in optional_inputs
    assert "subject" in optional_inputs
    assert "instructions" in optional_inputs
    assert "xml_string" in optional_inputs

    # Check hidden inputs
    assert "prompt" in hidden_inputs
    assert "extra_pnginfo" in hidden_inputs
