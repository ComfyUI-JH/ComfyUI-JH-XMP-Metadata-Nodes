from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.jh_save_image_with_xmp_metadata_node import (
    JHSaveImageWithXMPMetadataNode,
    JHSupportedImageTypes,
)


def test_save_images_no_images():
    node = JHSaveImageWithXMPMetadataNode()
    with pytest.raises(ValueError, match="No images to save."):
        node.save_images(images=[])


def test_save_images_with_metadata():
    node = JHSaveImageWithXMPMetadataNode()
    mock_image = MagicMock()
    mock_image.cpu.return_value.numpy.return_value = np.zeros((64, 64, 3))

    with patch(
        "folder_paths.get_save_image_path",
        return_value=("output", "file", 1, "subfolder", "prefix"),
    ):
        with patch("PIL.Image.Image.save") as mock_save:
            node.save_images(
                images=[mock_image],
                filename_prefix="Test",
                image_type=JHSupportedImageTypes.PNG,
                creator="Test Creator",
                title="Test Title",
                description="Test Description",
                subject="Test Subject",
                instructions="Test Instructions",
            )
            mock_save.assert_called_once()


def test_save_images_invalid_image_type():
    node = JHSaveImageWithXMPMetadataNode()
    mock_image = MagicMock()
    mock_image.cpu.return_value.numpy.return_value = np.zeros((64, 64, 3))

    with pytest.raises(ValueError, match="Unsupported image type"):
        node.save_images(
            images=[mock_image],
            filename_prefix="Test",
            image_type="INVALID_TYPE",  # Invalid image type
        )


def test_save_images_batch():
    node = JHSaveImageWithXMPMetadataNode()
    mock_image = MagicMock()
    mock_image.cpu.return_value.numpy.return_value = np.zeros((64, 64, 3))

    with patch(
        "folder_paths.get_save_image_path",
        return_value=("output", "file", 1, "subfolder", "prefix"),
    ):
        with patch("PIL.Image.Image.save") as mock_save:
            node.save_images(
                images=[mock_image, mock_image],
                filename_prefix="BatchTest",
                image_type=JHSupportedImageTypes.JPEG,
                creator=["Creator 1", "Creator 2"],
                title=["Title 1", "Title 2"],
            )
            assert mock_save.call_count == 2


def test_save_images_with_prompt_and_workflow():
    node = JHSaveImageWithXMPMetadataNode()
    mock_image = MagicMock()
    mock_image.cpu.return_value.numpy.return_value = np.zeros((64, 64, 3))

    with patch(
        "folder_paths.get_save_image_path",
        return_value=("output", "file", 1, "subfolder", "prefix"),
    ):
        with patch("PIL.Image.Image.save") as mock_save:
            node.save_images(
                images=[mock_image],
                filename_prefix="PromptWorkflowTest",
                image_type=JHSupportedImageTypes.PNG_WITH_WORKFLOW,
                prompt="Test Prompt",
                extra_pnginfo={"workflow": {"step": 1}},
            )
            mock_save.assert_called_once()


def test_save_images_empty_metadata():
    node = JHSaveImageWithXMPMetadataNode()
    mock_image = MagicMock()
    mock_image.cpu.return_value.numpy.return_value = np.zeros((64, 64, 3))

    with patch(
        "folder_paths.get_save_image_path",
        return_value=("output", "file", 1, "subfolder", "prefix"),
    ):
        with patch("PIL.Image.Image.save") as mock_save:
            node.save_images(
                images=[mock_image],
                filename_prefix="EmptyMetadataTest",
                image_type=JHSupportedImageTypes.PNG,
                creator="",
                title=None,
                description="",
                subject=None,
                instructions="",
            )
            mock_save.assert_called_once()


def test_save_images_mismatched_metadata_lengths():
    node = JHSaveImageWithXMPMetadataNode()
    mock_image = MagicMock()
    mock_image.cpu.return_value.numpy.return_value = np.zeros((64, 64, 3))

    with patch(
        "folder_paths.get_save_image_path",
        return_value=("output", "file", 1, "subfolder", "prefix"),
    ):
        with patch("PIL.Image.Image.save") as mock_save:
            with pytest.raises(IndexError):
                node.save_images(
                    images=[mock_image, mock_image],
                    filename_prefix="MismatchTest",
                    image_type=JHSupportedImageTypes.PNG,
                    creator=["Creator 1"],  # Fewer creators than images
                    title=["Title 1", "Title 2"],
                )
            mock_save.assert_called_once()
