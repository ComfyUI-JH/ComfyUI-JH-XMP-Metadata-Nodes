from unittest.mock import MagicMock, patch

import pytest
import torch

from src.jh_load_image_with_xmp_metadata_node import JHLoadImageWithXMPMetadataNode
from src.jh_xmp_metadata import JHXMPMetadata


def test_input_types():
    with patch("folder_paths.get_input_directory", return_value="test_dir"):
        with patch("os.listdir", return_value=["image1.jpg", "image2.png"]):
            with patch(
                "os.path.isfile", return_value=True
            ):  # Ensure files are recognized as files
                result = JHLoadImageWithXMPMetadataNode.INPUT_TYPES()
                assert "image" in result["required"]
                assert sorted(result["required"]["image"][0]) == [
                    "image1.jpg",
                    "image2.png",
                ]


def test_load_image_without_metadata():
    mock_image = MagicMock()
    mock_image.size = (64, 64)
    mock_image.mode = "RGB"
    mock_image.getbands.return_value = ["R", "G", "B"]
    mock_image.info = {}  # Ensure info is an empty dictionary

    with patch("folder_paths.get_annotated_filepath", return_value="test_image.jpg"):
        with patch("PIL.Image.open", return_value=mock_image):
            with patch("PIL.ImageSequence.Iterator", return_value=[mock_image]):
                result = JHLoadImageWithXMPMetadataNode().load_image("test_image.jpg")
                assert isinstance(result[0], torch.Tensor)
                assert isinstance(result[1], torch.Tensor)
                assert result[2:] == (None, None, None, None, None, None)


def test_load_image_with_metadata():
    mock_image = MagicMock()
    mock_image.size = (64, 64)
    mock_image.mode = "RGB"
    mock_image.getbands.return_value = ["R", "G", "B"]
    mock_image.info = {"xmp": b"<x:xmpmeta><rdf:RDF></rdf:RDF></x:xmpmeta>"}

    with patch("folder_paths.get_annotated_filepath", return_value="test_image.jpg"):
        with patch("PIL.Image.open", return_value=mock_image):
            with patch("PIL.ImageSequence.Iterator", return_value=[mock_image]):
                with patch(
                    "src.jh_xmp_metadata.JHXMPMetadata.from_string"
                ) as mock_metadata:
                    mock_metadata.return_value = JHXMPMetadata()
                    mock_metadata.return_value.creator = "Test Creator"
                    mock_metadata.return_value.title = "Test Title"
                    mock_metadata.return_value.description = "Test Description"
                    mock_metadata.return_value.subject = "Test Subject"
                    mock_metadata.return_value.instructions = "Test Instructions"

                    result = JHLoadImageWithXMPMetadataNode().load_image(
                        "test_image.jpg"
                    )

                    assert isinstance(result[0], torch.Tensor)
                    assert isinstance(result[1], torch.Tensor)
                    assert result[2:] == (
                        "Test Creator",
                        "Test Title",
                        "Test Description",
                        "Test Subject",
                        "Test Instructions",
                        mock_image.info["xmp"].decode("utf-8"),
                    )


def test_load_corrupted_image():
    with patch(
        "folder_paths.get_annotated_filepath", return_value="corrupted_image.jpg"
    ):
        with patch("PIL.Image.open", side_effect=OSError("Corrupted file")):
            with pytest.raises(OSError, match="Corrupted file"):
                JHLoadImageWithXMPMetadataNode().load_image("corrupted_image.jpg")


def test_integration_workflow():
    mock_image = MagicMock()
    mock_image.size = (128, 128)
    mock_image.mode = "RGB"
    mock_image.getbands.return_value = ["R", "G", "B"]
    mock_image.info = {"xmp": b"<x:xmpmeta><rdf:RDF></rdf:RDF></x:xmpmeta>"}

    with patch("folder_paths.get_annotated_filepath", return_value="test_image.jpg"):
        with patch("PIL.Image.open", return_value=mock_image):
            with patch("PIL.ImageSequence.Iterator", return_value=[mock_image]):
                with patch(
                    "src.jh_xmp_metadata.JHXMPMetadata.from_string"
                ) as mock_metadata:
                    mock_metadata.return_value = JHXMPMetadata()
                    mock_metadata.return_value.creator = "Integrated Creator"
                    mock_metadata.return_value.title = "Integrated Title"
                    mock_metadata.return_value.description = "Integrated Description"
                    mock_metadata.return_value.subject = "Integrated Subject"
                    mock_metadata.return_value.instructions = "Integrated Instructions"

                    result = JHLoadImageWithXMPMetadataNode().load_image(
                        "test_image.jpg"
                    )

                    assert isinstance(result[0], torch.Tensor)
                    assert result[0].shape == torch.Size([1, 0])
                    assert isinstance(result[1], torch.Tensor)
                    assert result[1].shape == torch.Size([1, 64, 64])
                    assert result[2:] == (
                        "Integrated Creator",
                        "Integrated Title",
                        "Integrated Description",
                        "Integrated Subject",
                        "Integrated Instructions",
                        mock_image.info["xmp"].decode("utf-8"),
                    )


def test_is_changed():
    with patch("folder_paths.get_annotated_filepath", return_value="test_image.jpg"):
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                b"image data"
            )
            result = JHLoadImageWithXMPMetadataNode.IS_CHANGED("test_image.jpg")
            assert isinstance(result, str)
            assert len(result) == 64  # SHA-256 hash length


def test_validate_inputs():
    with patch("folder_paths.exists_annotated_filepath", return_value=True):
        result = JHLoadImageWithXMPMetadataNode.VALIDATE_INPUTS("test_image.jpg")
        assert result is True

    with patch("folder_paths.exists_annotated_filepath", return_value=False):
        result = JHLoadImageWithXMPMetadataNode.VALIDATE_INPUTS("missing_image.jpg")
        assert result == "Invalid image file: missing_image.jpg"
