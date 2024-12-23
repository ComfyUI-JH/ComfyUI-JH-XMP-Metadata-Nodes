from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pytest
import torch
from PIL import Image
from pytest_mock import MockerFixture

from comfyui_jh_xmp_metadata_nodes.jh_save_image_with_xmp_metadata_node import (
    JHSaveImageWithXMPMetadataNode,
    JHSupportedImageTypes,
)


@pytest.fixture
def mock_folder_paths(mocker: MockerFixture) -> dict[str, MagicMock | AsyncMock]:
    mock_get_output_dir = mocker.patch(
        "folder_paths.get_output_directory", return_value="/mock/output/dir"
    )
    mock_get_save_path = mocker.patch(
        "folder_paths.get_save_image_path",
        return_value=(
            "/mock/output/dir",
            "mock_filename",
            0,
            "mock_subfolder",
            "mock_filename_prefix",
        ),
    )

    # Return a dictionary of mocks so you can access them in tests
    return {
        "get_output_directory": mock_get_output_dir,
        "get_save_image_path": mock_get_save_path,
    }


@pytest.fixture
def image() -> torch.Tensor:
    return torch.rand(100, 100, 3)  # Generate a random 3-channel tensor


@pytest.fixture
def node() -> JHSaveImageWithXMPMetadataNode:
    return JHSaveImageWithXMPMetadataNode()


def test_save_images_no_images(node: JHSaveImageWithXMPMetadataNode) -> None:
    with pytest.raises(ValueError, match="No images to save."):
        node.save_images([])


@pytest.mark.parametrize(
    "image_type,expected_extension",
    [
        (JHSupportedImageTypes.JPEG, ".jpg"),
        (JHSupportedImageTypes.PNG, ".png"),
        (JHSupportedImageTypes.PNG_WITH_WORKFLOW, ".png"),
        (JHSupportedImageTypes.WEBP, ".webp"),
        (JHSupportedImageTypes.LOSSLESS_WEBP, ".webp"),
    ],
)
def test_save_image(
    node: JHSaveImageWithXMPMetadataNode,
    image: torch.Tensor,
    tmp_path: Path,
    image_type: JHSupportedImageTypes,
    expected_extension: str,
) -> None:
    img = Image.fromarray((image.numpy() * 255).astype(np.uint8))
    to_path = tmp_path / f"test_image{expected_extension}"
    xmp = "<xmpmeta>Test XML</xmpmeta>"
    prompt = "Test Prompt"
    extra_pnginfo = {"workflow": "Test Workflow"}

    node.save_image(img, image_type, to_path, xmp, prompt, extra_pnginfo)

    assert to_path.exists()
    assert to_path.suffix == expected_extension


def test_save_images_with_metadata(
    node: JHSaveImageWithXMPMetadataNode,
    image: torch.Tensor,
    mock_folder_paths: dict[str, MagicMock],
) -> None:
    images = [image]
    mock_save_image = MagicMock()
    node.save_image = mock_save_image

    result = node.save_images(
        images,
        image_type=JHSupportedImageTypes.PNG,
        creator="Test Creator",
        title="Test Title",
        description="Test Description",
    )

    assert len(result["result"]) == 1
    assert len(result["result"][0]) == 1
    assert isinstance(result["result"][0][0], torch.Tensor)

    assert len(result["ui"]["images"]) == 1
    assert result["ui"]["images"][0]["filename"].endswith(".png")

    mock_save_image.assert_called_once()


def test_extension_for_type(node: JHSaveImageWithXMPMetadataNode) -> None:
    assert node.extension_for_type(JHSupportedImageTypes.JPEG) == "jpeg"
    assert node.extension_for_type(JHSupportedImageTypes.PNG) == "png"
    assert node.extension_for_type(JHSupportedImageTypes.LOSSLESS_WEBP) == "webp"
    assert node.extension_for_type(JHSupportedImageTypes.WEBP) == "webp"
    assert node.extension_for_type(JHSupportedImageTypes.PNG_WITH_WORKFLOW) == "png"


def test_inputs_to_xml_with_xml_string(node: JHSaveImageWithXMPMetadataNode) -> None:
    xml_string = "<xmpmeta>Test XML</xmpmeta>"
    result = node.inputs_to_xml(
        creator=None,
        rights=None,
        title=None,
        description=None,
        subject=None,
        instructions=None,
        comment=None,
        alt_text=None,
        ext_description=None,
        xml_string=xml_string,
        batch_number=0,
    )
    assert result == xml_string


def test_inputs_to_xml_with_metadata_fields(
    node: JHSaveImageWithXMPMetadataNode,
) -> None:
    result = node.inputs_to_xml(
        creator="Test Creator",
        rights="Test Rights",
        title="Test Title",
        description="Test Description",
        subject="Test Subject",
        instructions="Test Instructions",
        comment="Test Comment",
        alt_text="Test Alt Text",
        ext_description="Test Ext Description",
        xml_string=None,
        batch_number=0,
    )
    assert "Test Creator" in result
    assert "Test Rights" in result
    assert "Test Title" in result
    assert "Test Description" in result
    assert "Test Subject" in result
    assert "Test Instructions" in result
    assert "Test Comment" in result
    assert "Test Alt Text" in result
    assert "Test Ext Description" in result


def test_inputs_to_xml_with_list_metadata_fields(
    node: JHSaveImageWithXMPMetadataNode,
) -> None:
    result = node.inputs_to_xml(
        creator=["Creator 1", "Creator 2"],
        rights=["Rights 1", "Rights 2"],
        title=["Title 1", "Title 2"],
        description=["Description 1", "Description 2"],
        subject=["Subject 1", "Subject 2"],
        instructions=["Instructions 1", "Instructions 2"],
        comment=["Comment 1", "Comment 2"],
        alt_text=["Alt Text 1", "Alt Text 2"],
        ext_description=["Ext Description 1", "Ext Description 2"],
        xml_string=None,
        batch_number=1,
    )
    assert "Creator 2" in result
    assert "Rights 2" in result
    assert "Title 2" in result
    assert "Description 2" in result
    assert "Subject 2" in result
    assert "Instructions 2" in result
    assert "Comment 2" in result
    assert "Alt Text 2" in result
    assert "Ext Description 2" in result


def test_input_types(node: JHSaveImageWithXMPMetadataNode) -> None:
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
    assert "rights" in optional_inputs
    assert "title" in optional_inputs
    assert "description" in optional_inputs
    assert "subject" in optional_inputs
    assert "instructions" in optional_inputs
    assert "comment" in optional_inputs
    assert "alt_text" in optional_inputs
    assert "xml_string" in optional_inputs

    # Check hidden inputs
    assert "prompt" in hidden_inputs
    assert "extra_pnginfo" in hidden_inputs
