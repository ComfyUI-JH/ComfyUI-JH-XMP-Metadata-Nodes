import pytest
from src.jh_xmp_metadata import JHXMPMetadata

def test_init():
    metadata = JHXMPMetadata()
    assert metadata.creator is None
    assert metadata.title is None
    assert metadata.description is None
    assert metadata.subject is None
    assert metadata.instructions is None
    assert metadata.make is None
    assert metadata.model is None

def test_set_creator():
    metadata = JHXMPMetadata()
    metadata.creator = "John Doe"
    assert metadata._creator == "John Doe"

def test_set_title():
    metadata = JHXMPMetadata()
    metadata.title = "My Title"
    assert metadata._title == "My Title"

def test_set_description():
    metadata = JHXMPMetadata()
    metadata._description = "My Description"
    assert metadata._description == "My Description"

def test_set_subject():
    metadata = JHXMPMetadata()
    metadata.subject = "My Subject"
    assert metadata._subject == "My Subject"

def test_set_instructions():
    metadata = JHXMPMetadata()
    metadata.instructions = "My Instructions"
    assert metadata._instructions == "My Instructions"

def test_set_make():
    metadata = JHXMPMetadata()
    metadata.make = "My Make"
    assert metadata._make == "My Make"

def test_set_model():
    metadata = JHXMPMetadata()
    metadata.model = "My Model"
    assert metadata._model == "My Model"

def test_to_string():
    metadata = JHXMPMetadata()
    metadata.creator = "John Doe"
    metadata.title = "My Title"
    metadata.description = "My Description"
    metadata.subject = "My Subject"
    metadata.instructions = "My Instructions"
    metadata.make = "My Make"
    metadata.model = "My Model"
    xml_string = metadata.to_string()
    assert "John Doe" in xml_string
    assert "My Title" in xml_string
    assert "My Description" in xml_string
    assert "My Subject" in xml_string
    assert "My Instructions" in xml_string
    assert "My Make" in xml_string
    assert "My Model" in xml_string

def test_to_wrapped_string():
    metadata = JHXMPMetadata()
    metadata.creator = "John Doe"
    metadata.title = "My Title"
    metadata.description = "My Description"
    metadata.subject = "My Subject"
    metadata.instructions = "My Instructions"
    metadata.make = "My Make"
    metadata.model = "My Model"
    wrapped_string = metadata.to_wrapped_string()
    assert wrapped_string.startswith("<?xpacket")
    assert "John Doe" in wrapped_string
    assert "My Title" in wrapped_string
    assert "My Description" in wrapped_string
    assert "My Subject" in wrapped_string
    assert "My Instructions" in wrapped_string
    assert "My Make" in wrapped_string
    assert "My Model" in wrapped_string