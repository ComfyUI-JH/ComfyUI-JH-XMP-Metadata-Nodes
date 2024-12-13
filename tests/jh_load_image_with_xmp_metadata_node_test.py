import pytest
from unittest.mock import patch, mock_open, MagicMock
import torch
import numpy as np
from src.jh_load_image_with_xmp_metadata_node import JHLoadImageWithXMPMetadataNode


@pytest.fixture
def sample_image_path():
    return "sample_image.jpg"


@pytest.fixture
def sample_xmp_metadata():
    return """
    <x:xmpmeta xmlns:x="adobe:ns:meta/">
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description xmlns:dc="http://purl.org/dc/elements/1.1/">
                <dc:creator>
                    <rdf:Seq>
                        <rdf:li>John Doe</rdf:li>
                    </rdf:Seq>
                </dc:creator>
                <dc:title>
                    <rdf:Alt>
                        <rdf:li>Sample Title</rdf:li>
                    </rdf:Alt>
                </dc:title>
                <dc:description>
                    <rdf:Alt>
                        <rdf:li>Sample Description</rdf:li>
                    </rdf:Alt>
                </dc:description>
            </rdf:Description>
        </rdf:RDF>
    </x:xmpmeta>
    """


@patch("folder_paths.get_annotated_filepath", return_value="mocked_image.jpg")
@patch("os.path.isfile", return_value=True)
@patch("os.listdir", return_value=["mocked_image.jpg"])
@patch("PIL.Image.open")
def test_load_image_with_metadata(mock_image_open, mock_listdir, mock_isfile, mock_get_annotated_filepath, sample_xmp_metadata):
    # Mocking the image and its metadata
    mock_image = MagicMock()
    mock_image.info = {"xmp": sample_xmp_metadata}
    mock_image.format = "JPEG"
    mock_image.size = (64, 64)
    mock_image.getbands = MagicMock(return_value="RGB")
    mock_image.getchannel = MagicMock(return_value=np.zeros((64, 64)))
    mock_image_open.return_value = mock_image

    # Limit frames to a few iterations
    mock_iterator = [mock_image] * 3  # Simulate 3 frames
    patch("PIL.ImageSequence.Iterator", return_value=mock_iterator).start()

    node = JHLoadImageWithXMPMetadataNode()
    result = node.load_image("mocked_image.jpg")

    assert len(result) == 7  # Ensure the method returns 7 outputs
    assert isinstance(result[0], torch.Tensor)  # IMAGE
    assert isinstance(result[1], torch.Tensor)  # MASK
    assert result[2] == "John Doe"  # creator
    assert result[3] == "Sample Title"  # title
    assert result[4] == "Sample Description"  # description


@patch("folder_paths.exists_annotated_filepath", return_value=True)
def test_validate_inputs_success(mock_exists_annotated_filepath, sample_image_path):
    node = JHLoadImageWithXMPMetadataNode()
    result = node.VALIDATE_INPUTS(sample_image_path)
    assert result is True  # Validation passes


@patch("folder_paths.exists_annotated_filepath", return_value=False)
def test_validate_inputs_failure(mock_exists_annotated_filepath, sample_image_path):
    node = JHLoadImageWithXMPMetadataNode()
    result = node.VALIDATE_INPUTS(sample_image_path)
    assert result == f"Invalid image file: {sample_image_path}"  # Validation fails


@patch("builtins.open", new_callable=mock_open, read_data=b"dummy data")
@patch("folder_paths.get_annotated_filepath", return_value="mocked_image.jpg")
def test_is_changed(mock_get_annotated_filepath, mock_file_open, sample_image_path):
    node = JHLoadImageWithXMPMetadataNode()
    result = node.IS_CHANGED(sample_image_path)
    assert isinstance(result, str)  # Should return a SHA-256 hash as a string
    assert len(result) == 64  # SHA-256 hashes are 64 hex characters long
