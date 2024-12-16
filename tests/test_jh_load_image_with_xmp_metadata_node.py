import numpy as np
import pytest
import torch
from PIL import Image

from src.jh_load_image_with_xmp_metadata_node import JHLoadImageWithXMPMetadataNode

# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


@pytest.fixture
def valid_frame() -> Image.Image:
    # Create a valid RGB image with an alpha channel
    width, height = 64, 64
    data = np.random.randint(0, 255, (height, width, 4), dtype=np.uint8)
    return Image.fromarray(data, "RGBA")


@pytest.fixture
def int_frame() -> Image.Image:
    # Create a valid 32-bit integer image
    width, height = 64, 64
    data = np.random.randint(0, 65535, (height, width), dtype=np.uint32)
    return Image.fromarray(data, "I")


@pytest.fixture
def different_size_frame() -> Image.Image:
    # Create a valid RGB image with an alpha channel but different size
    width, height = 128, 128
    data = np.random.randint(0, 255, (height, width, 4), dtype=np.uint8)
    return Image.fromarray(data, "RGBA")


def test_frame_to_tensors(valid_frame: Image.Image):
    node = JHLoadImageWithXMPMetadataNode()
    image_size = valid_frame.size

    image_tensor, mask_tensor = node._frame_to_tensors(valid_frame, image_size)

    assert image_tensor is not None, "Image tensor should not be None"
    assert mask_tensor is not None, "Mask tensor should not be None"
    assert image_tensor.shape == (1, 64, 64, 3), "Image tensor shape is incorrect"
    assert mask_tensor.shape == (64, 64), "Mask tensor shape is incorrect"
    assert image_tensor.dtype == torch.float32, "Image tensor dtype is incorrect"
    assert mask_tensor.dtype == torch.float32, "Mask tensor dtype is incorrect"
    assert torch.all(
        (image_tensor >= 0) & (image_tensor <= 1)
    ), "Image tensor values should be in [0, 1]"
    assert torch.all(
        (mask_tensor >= 0) & (mask_tensor <= 1)
    ), "Mask tensor values should be in [0, 1]"


def test_frame_to_tensors_int_mode(int_frame: Image.Image):
    node = JHLoadImageWithXMPMetadataNode()
    image_size = int_frame.size

    image_tensor, mask_tensor = node._frame_to_tensors(int_frame, image_size)

    assert image_tensor is not None, "Image tensor should not be None"
    assert mask_tensor is not None, "Mask tensor should not be None"
    assert image_tensor.shape == (1, 64, 64, 3), "Image tensor shape is incorrect"
    assert mask_tensor.shape == (64, 64), "Mask tensor shape is incorrect"
    assert image_tensor.dtype == torch.float32, "Image tensor dtype is incorrect"
    assert mask_tensor.dtype == torch.float32, "Mask tensor dtype is incorrect"
    assert torch.all(
        (image_tensor >= 0) & (image_tensor <= 1)
    ), "Image tensor values should be in [0, 1]"
    assert torch.all(
        (mask_tensor >= 0) & (mask_tensor <= 1)
    ), "Mask tensor values should be in [0, 1]"


def test_frame_to_tensors_different_size(different_size_frame: Image.Image):
    node = JHLoadImageWithXMPMetadataNode()
    image_size = (64, 64)

    image_tensor, mask_tensor = node._frame_to_tensors(different_size_frame, image_size)

    assert image_tensor is None, "Image tensor should be None for different size frame"
    assert mask_tensor is None, "Mask tensor should be None for different size frame"
