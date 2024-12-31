from pathlib import Path

import numpy as np
import pytest
import torch
from PIL import Image
from pytest_mock import MockerFixture

from comfyui_jh_xmp_metadata_nodes.jh_save_image_with_xmp_metadata_node import (
    JHSaveImageWithXMPMetadataNode,
    JHSupportedImageTypes,
)

# region Fixtures


@pytest.fixture
def image() -> torch.Tensor:
    return torch.rand(100, 100, 3)  # Generate a random 3-channel tensor


@pytest.fixture
def node() -> JHSaveImageWithXMPMetadataNode:
    return JHSaveImageWithXMPMetadataNode()


# endregion Fixtures

# region Tests


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
    civitai_metadata = "Test Civitai Metadata"
    xmp = "<xmpmeta>Test XML</xmpmeta>"
    prompt = "Test Prompt"
    extra_pnginfo = {"workflow": "Test Workflow"}

    node.save_image(
        img, image_type, to_path, civitai_metadata, xmp, prompt, extra_pnginfo
    )

    assert to_path.exists()
    assert to_path.suffix == expected_extension


def test_save_images_with_metadata(
    mocker: MockerFixture,
    tmp_path: Path,
    node: JHSaveImageWithXMPMetadataNode,
    image: torch.Tensor,
) -> None:
    mocker.patch(
        "comfyui_jh_xmp_metadata_nodes.jh_save_image_with_xmp_metadata_node.folder_paths.get_save_image_path",
        return_value=(
            tmp_path,
            "ComfyUI",
            2160,
            "",
            "ComfyUI",
        ),
    )

    images = [image]

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
    assert "alt_text" in optional_inputs
    assert "xml_string" in optional_inputs

    # Check hidden inputs
    assert "prompt" in hidden_inputs
    assert "extra_pnginfo" in hidden_inputs


# endregion Tests
