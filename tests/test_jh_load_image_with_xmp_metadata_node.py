import hashlib
from pathlib import Path

import PIL.Image
import pytest
import torch
from pytest_mock import MockerFixture

from comfyui_jh_xmp_metadata_nodes.jh_load_image_with_xmp_metadata_node import (
    JHLoadImageWithXMPMetadataNode,
)

# region Fixtures


@pytest.fixture
def valid_xml_string() -> str:
    return """
    <x:xmpmeta xmlns:x="adobe:ns:meta/">
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about=""
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
                xmlns:exif="http://ns.adobe.com/exif/1.0/"
                xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">
                <dc:creator>
                    <rdf:Seq>
                        <rdf:li>Test Creator</rdf:li>
                    </rdf:Seq>
                </dc:creator>
                <dc:rights>
                    <rdf:Alt>
                        <rdf:li xml:lang="x-default">Test Rights</rdf:li>
                    </rdf:Alt>
                </dc:rights>
                <dc:title>
                    <rdf:Alt>
                        <rdf:li xml:lang="x-default">Test Title</rdf:li>
                    </rdf:Alt>
                </dc:title>
                <dc:description>
                    <rdf:Alt>
                        <rdf:li xml:lang="x-default">Test Description</rdf:li>
                    </rdf:Alt>
                </dc:description>
                <dc:subject>
                    <rdf:Bag>
                        <rdf:li>Test Subject</rdf:li>
                    </rdf:Bag>
                </dc:subject>
                <photoshop:Instructions>Test Instructions</photoshop:Instructions>
                <exif:UserComment>
                    <rdf:Alt>
                        <rdf:li xml:lang="x-default">Test Comment</rdf:li>
                    </rdf:Alt>
                </exif:UserComment>
                <Iptc4xmpCore:AltTextAccessibility>Test Alt Text</Iptc4xmpCore:AltTextAccessibility>
                <Iptc4xmpCore:ExtDescrAccessibility>Test Ext Description</Iptc4xmpCore:ExtDescrAccessibility>
            </rdf:Description>
        </rdf:RDF>
    </x:xmpmeta>
    """  # noqa: E501


@pytest.fixture
def invalid_xml_string() -> str:
    return "This is not XML."


@pytest.fixture
def sample_image_file_with_valid_xmp_metadata(
    tmp_path: Path, valid_xml_string: str
) -> Path:
    img_path = tmp_path / "test_image_valid_xml.webp"
    image = PIL.Image.new(
        "RGBA", (64, 64), color=(255, 0, 0, 128)
    )  # Red image with alpha
    image.save(img_path, xmp=valid_xml_string)  # Save with XMP metadata
    return img_path


@pytest.fixture
def sample_image_file_with_invalid_xmp_metadata(
    tmp_path: Path, invalid_xml_string: str
) -> Path:
    img_path = tmp_path / "test_image_invalid_xml.webp"
    image = PIL.Image.new(
        "RGBA", (64, 64), color=(255, 0, 0, 128)
    )  # Red image with alpha
    image.save(img_path, xmp=invalid_xml_string)  # Save with invalid XMP metadata
    return img_path


@pytest.fixture
def sample_image_file_with_garbage_xmp_metadata(
    tmp_path: Path, garbage_xml_string: str
) -> Path:
    img_path = tmp_path / "test_image_garbage_xml.webp"
    image = PIL.Image.new(
        "RGBA", (64, 64), color=(255, 0, 0, 128)
    )  # Red image with alpha
    image.save(img_path, xmp=garbage_xml_string)  # Save with invalid XMP metadata
    return img_path


@pytest.fixture
def sample_multiframe_image_file(tmp_path: Path) -> Path:
    img_path = tmp_path / "test_image_multiframe.png"

    # Create multiple frames
    frames = [
        PIL.Image.new("RGBA", (64, 64), color=(255, 0, 0, 128)),  # Red with alpha
        PIL.Image.new("RGBA", (64, 64), color=(0, 255, 0, 128)),  # Green with alpha
        PIL.Image.new("RGBA", (64, 64), color=(0, 0, 255, 128)),  # Blue with alpha
    ]

    # Save as an animated PNG (APNG)
    frames[0].save(
        img_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # Frame duration in ms
        loop=0,  # Infinite loop
    )
    return img_path


@pytest.fixture
def sample_invalid_multiframe_image_file(tmp_path: Path) -> Path:
    """
    Frankly I admire Comfy for considering this possibility. An APNG
    _can't_ have frames of different sizes because they all get padded
    to the largest frame's size. In order to test this scenario we have
    to use a different format, like TIFF, which _can_ have frames of
    different sizes but which is not well supported by ComfyUI at this
    time.
    """
    img_path = tmp_path / "test_image_multiframe_different_size.tiff"

    # Create frames with different sizes
    frame1 = PIL.Image.new("RGBA", (64, 64), color=(255, 0, 0, 128))
    frame2 = PIL.Image.new("RGBA", (32, 32), color=(0, 255, 0, 128))
    frame3 = PIL.Image.new("RGBA", (64, 64), color=(0, 0, 255, 128))

    # Save as multi-frame TIFF
    frame1.save(
        img_path,
        save_all=True,
        append_images=[frame2, frame3],
        compression="tiff_deflate",  # Optional compression
    )

    return img_path


@pytest.fixture
def sample_rgb_image_file(tmp_path: Path) -> Path:
    img_path = tmp_path / "test_image_rgb.png"
    image = PIL.Image.new("RGB", (64, 64))  # RGB image
    image.save(img_path)
    return img_path


@pytest.fixture
def sample_grayscale_image_file(tmp_path: Path) -> Path:
    img_path = tmp_path / "test_image_grayscale.png"
    image = PIL.Image.new("L", (64, 64))  # Grayscale image
    image.save(img_path)
    return img_path


@pytest.fixture
def sample_32_bit_integer_image_file(tmp_path: Path) -> Path:
    img_path = tmp_path / "test_image_32_bit_integer.png"
    image = PIL.Image.new("I", (64, 64))  # 32-bit integer image
    image.save(img_path)
    return img_path


@pytest.fixture
def sample_corrupted_image_file(tmp_path: Path) -> Path:
    corrupted_file = tmp_path / "corrupted_image.png"
    with open(corrupted_file, "wb") as f:
        f.write(b"This is not a valid image file.")
    return corrupted_file


# endregion Fixtures


def test_input_types(mocker: MockerFixture) -> None:
    mocker.patch("folder_paths.get_input_directory", return_value="/mocked/path")
    mocker.patch("os.listdir", return_value=["img1.png", "img2.png"])
    mocker.patch("os.path.isfile", return_value=True)

    input_types = JHLoadImageWithXMPMetadataNode.INPUT_TYPES()
    assert input_types.keys() == {"required"}
    assert "required" in input_types and input_types["required"].keys() == {"image"}


def test_get_image_files(mocker: MockerFixture) -> None:
    mocker.patch("folder_paths.get_input_directory", return_value="/mocked/path")
    mocker.patch("os.listdir", return_value=["img1.png", "img2.png", "img3.png"])
    mocker.patch("os.path.isfile", return_value=True)

    files = JHLoadImageWithXMPMetadataNode.get_image_files()
    assert files == ["img1.png", "img2.png", "img3.png"]


def test_get_image_files_with_non_files(mocker: MockerFixture) -> None:
    mocker.patch("folder_paths.get_input_directory", return_value="/mocked/path")
    mocker.patch("os.listdir", return_value=["img1.png", "directory", "img3.png"])
    mocker.patch("os.path.isfile", side_effect=lambda p: not p.endswith("directory"))

    files = JHLoadImageWithXMPMetadataNode.get_image_files()
    assert files == ["img1.png", "img3.png"]


def test_validate_inputs_valid_file(
    mocker: MockerFixture,
    sample_image_file_with_valid_xmp_metadata: Path,
) -> None:
    mocker.patch("folder_paths.exists_annotated_filepath", return_value=True)

    assert (
        JHLoadImageWithXMPMetadataNode.VALIDATE_INPUTS(
            sample_image_file_with_valid_xmp_metadata.name
        )
        is True
    )


def test_validate_inputs_invalid_file(mocker: MockerFixture) -> None:
    mocker.patch("folder_paths.exists_annotated_filepath", return_value=False)

    result = JHLoadImageWithXMPMetadataNode.VALIDATE_INPUTS("nonexistent.png")
    assert result == "Invalid image file: nonexistent.png"


def test_frame_to_tensors() -> None:
    node = JHLoadImageWithXMPMetadataNode()
    image = PIL.Image.new("RGBA", (64, 64), color=(255, 255, 255, 128))
    tensor_image, tensor_mask = node._frame_to_tensors(image)

    assert tensor_image is not None
    assert tensor_mask is not None
    assert tensor_image.shape == (1, 64, 64, 3)
    assert tensor_mask.shape == (64, 64)
    assert torch.allclose(tensor_mask, torch.full((64, 64), 0.5), atol=0.01)


def test_load_image_with_valid_metadata(
    mocker: MockerFixture,
    sample_image_file_with_valid_xmp_metadata: Path,
    valid_xml_string: str,
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_image_file_with_valid_xmp_metadata),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_image_file_with_valid_xmp_metadata.name)

    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (1, 64, 64, 3)
    assert output.MASK.shape == (1, 64, 64)  # MASK
    assert output.creator == "Test Creator"  # creator
    assert output.rights == "Test Rights"  # rights
    assert output.title == "Test Title"  # title
    assert output.description == "Test Description"  # description
    assert output.subject == "Test Subject"  # subject
    assert output.instructions == "Test Instructions"  # instructions
    assert output.comment == "Test Comment"  # xml_string
    assert output.alt_text == "Test Alt Text"  # alt_text
    assert output.ext_description == "Test Ext Description"  # ext_description
    assert output.xml_string == valid_xml_string  # xml_string


def test_load_image_with_invalid_metadata(
    mocker: MockerFixture,
    sample_image_file_with_invalid_xmp_metadata: Path,
    invalid_xml_string: str,
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_image_file_with_invalid_xmp_metadata),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_image_file_with_invalid_xmp_metadata.name)

    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (1, 64, 64, 3)
    assert output.MASK.shape == (1, 64, 64)  # MASK
    assert output.creator is None  # creator
    assert output.rights is None  # rights
    assert output.title is None  # title
    assert output.description is None  # description
    assert output.subject is None  # subject
    assert output.instructions is None  # instructions
    assert output.comment is None  # comment
    assert output.alt_text is None  # alt_text
    assert output.ext_description is None  # ext_description
    assert output.xml_string == invalid_xml_string  # xml_string


def test_load_image_with_multiframe_image_file(
    mocker: MockerFixture,
    sample_multiframe_image_file: Path,
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_multiframe_image_file),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_multiframe_image_file.name)

    # Verify outputs
    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (3, 64, 64, 3)  # 3 frames, RGB
    assert output.MASK.shape == (3, 64, 64)  # 3 masks
    assert output.creator is None  # creator
    assert output.rights is None  # rights
    assert output.title is None  # title
    assert output.description is None  # description
    assert output.subject is None  # subject
    assert output.instructions is None  # instructions
    assert output.comment is None  # comment
    assert output.alt_text is None  # alt_text
    assert output.ext_description is None  # ext_description
    assert output.xml_string == ""  # xml_string


def test_load_image_with_invalid_multiframe_image_file(
    mocker: MockerFixture,
    sample_invalid_multiframe_image_file: Path,
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_invalid_multiframe_image_file),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_invalid_multiframe_image_file.name)

    # Verify outputs
    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (2, 64, 64, 3)  # 2 frames, RGB
    assert output.MASK.shape == (2, 64, 64)  # 2 masks
    assert output.creator is None  # creator
    assert output.rights is None  # rights
    assert output.title is None  # title
    assert output.description is None  # description
    assert output.subject is None  # subject
    assert output.instructions is None  # instructions
    assert output.comment is None  # comment
    assert output.alt_text is None  # alt_text
    assert output.ext_description is None  # ext_description
    assert output.xml_string == ""  # xml_string


def test_load_rgb_image(mocker: MockerFixture, sample_rgb_image_file: Path) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_rgb_image_file),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_rgb_image_file.name)

    # Verify outputs
    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (1, 64, 64, 3)  # 1 frame, RGB
    assert output.MASK.shape == (1, 64, 64)  # MASK
    assert output.creator is None  # creator
    assert output.rights is None  # rights
    assert output.title is None  # title
    assert output.description is None  # description
    assert output.subject is None  # subject
    assert output.instructions is None  # instructions
    assert output.comment is None  # comment
    assert output.alt_text is None  # alt_text
    assert output.ext_description is None  # ext_description
    assert output.xml_string == ""  # xml_string


def test_load_32_bit_integer_image(
    mocker: MockerFixture, sample_32_bit_integer_image_file: Path
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_32_bit_integer_image_file),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_32_bit_integer_image_file.name)

    # Verify outputs
    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (1, 64, 64, 3)  # 1 frame, RGB
    assert output.MASK.shape == (1, 64, 64)  # MASK
    assert output.creator is None  # creator
    assert output.rights is None  # rights
    assert output.title is None  # title
    assert output.description is None  # description
    assert output.subject is None  # subject
    assert output.instructions is None  # instructions
    assert output.comment is None  # comment
    assert output.alt_text is None  # alt_text
    assert output.ext_description is None  # ext_description
    assert output.xml_string == ""  # xml_string

    # Verify RGB channel consistency
    rgb_values = output.IMAGE[0, :, :, :]
    assert torch.allclose(rgb_values[:, :, 0], rgb_values[:, :, 1])  # R == G
    assert torch.allclose(rgb_values[:, :, 1], rgb_values[:, :, 2])  # G == B
    assert torch.allclose(rgb_values[:, :, 0], rgb_values[:, :, 2])  # R == B

    # Make sure RGB values are in [0, 1]
    assert torch.all(rgb_values >= 0) and torch.all(rgb_values <= 1)


def test_load_grayscale_image(
    mocker: MockerFixture, sample_grayscale_image_file: Path
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_grayscale_image_file),
    )

    node = JHLoadImageWithXMPMetadataNode()
    output = node.load_image(sample_grayscale_image_file.name)

    # Verify outputs
    assert isinstance(output.IMAGE, torch.Tensor)  # IMAGE
    assert output.IMAGE.shape == (1, 64, 64, 3)  # Converted to RGB
    assert output.MASK.shape == (1, 64, 64)  # MASK
    assert output.creator is None  # creator
    assert output.rights is None  # rights
    assert output.title is None  # title
    assert output.description is None  # description
    assert output.subject is None  # subject
    assert output.instructions is None  # instructions
    assert output.comment is None  # comment
    assert output.alt_text is None  # alt_text
    assert output.ext_description is None  # ext_description
    assert output.xml_string == ""  # xml_string

    # Verify that the image tensor is in RGB format
    assert output.IMAGE.shape[-1] == 3  # Last dimension should be 3 for RGB


def test_load_corrupted_image(
    mocker: MockerFixture, sample_corrupted_image_file: Path
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_corrupted_image_file),
    )

    node = JHLoadImageWithXMPMetadataNode()
    with pytest.raises(PIL.UnidentifiedImageError, match="cannot identify image file"):
        node.load_image(sample_corrupted_image_file.name)


def test_is_changed(
    mocker: MockerFixture, sample_image_file_with_valid_xmp_metadata: Path
) -> None:
    mocker.patch(
        "folder_paths.get_annotated_filepath",
        return_value=str(sample_image_file_with_valid_xmp_metadata),
    )

    expected_hash = hashlib.sha256(
        sample_image_file_with_valid_xmp_metadata.read_bytes()
    ).hexdigest()
    result = JHLoadImageWithXMPMetadataNode.IS_CHANGED(
        sample_image_file_with_valid_xmp_metadata.name
    )
    assert result == expected_hash


def test_is_changed_nonexistent_file(mocker: MockerFixture) -> None:
    mocker.patch("folder_paths.get_annotated_filepath", return_value="nonexistent.png")

    with pytest.raises(FileNotFoundError):
        JHLoadImageWithXMPMetadataNode.IS_CHANGED("nonexistent.png")
