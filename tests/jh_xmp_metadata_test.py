import pytest
from lxml import etree

from src.jh_xmp_metadata import JHXMPMetadata


@pytest.fixture
def xmp_metadata():
    return JHXMPMetadata()


def test_initial_state(xmp_metadata):
    assert xmp_metadata.creator is None
    assert xmp_metadata.title is None
    assert xmp_metadata.description is None
    assert xmp_metadata.subject is None
    assert xmp_metadata.instructions is None
    assert xmp_metadata.to_string() is not None


def test_creator_setter(xmp_metadata):
    xmp_metadata.creator = "Alice, Bob"
    assert xmp_metadata.creator == "Alice, Bob"
    xml = xmp_metadata.to_string()
    assert "<dc:creator" in xml
    assert "Alice" in xml
    assert "Bob" in xml


def test_creator_setter_invalid_data(xmp_metadata):
    with pytest.raises(TypeError):
        xmp_metadata.creator = 12345


def test_creator_setter_empty_string(xmp_metadata):
    xmp_metadata.creator = ""
    assert xmp_metadata.creator is None
    xml = xmp_metadata.to_string()
    assert "<dc:creator" not in xml


def test_title_setter(xmp_metadata):
    xmp_metadata.title = "Sample Title"
    assert xmp_metadata.title == "Sample Title"
    xml = xmp_metadata.to_string()
    assert "<dc:title" in xml
    assert "Sample Title" in xml


def test_title_setter_invalid_data(xmp_metadata):
    with pytest.raises(TypeError):
        xmp_metadata.title = 12345


def test_title_setter_empty_string(xmp_metadata):
    xmp_metadata.title = ""
    assert xmp_metadata.title is None
    xml = xmp_metadata.to_string()
    assert "<dc:title" not in xml


def test_description_setter(xmp_metadata):
    xmp_metadata.description = "Sample Description"
    assert xmp_metadata.description == "Sample Description"
    xml = xmp_metadata.to_string()
    assert "<dc:description" in xml
    assert "Sample Description" in xml


def test_description_setter_invalid_data(xmp_metadata):
    with pytest.raises(TypeError):
        xmp_metadata.description = 12345


def test_description_setter_empty_string(xmp_metadata):
    xmp_metadata.description = ""
    assert xmp_metadata.description is None
    xml = xmp_metadata.to_string()
    assert "<dc:description" not in xml


def test_subject_setter(xmp_metadata):
    xmp_metadata.subject = "Keyword1, Keyword2"
    assert xmp_metadata.subject == "Keyword1, Keyword2"
    xml = xmp_metadata.to_string()
    assert "<dc:subject" in xml
    assert "Keyword1" in xml
    assert "Keyword2" in xml


def test_subject_setter_invalid_data(xmp_metadata):
    with pytest.raises(TypeError):
        xmp_metadata.subject = 12345


def test_subject_setter_empty_string(xmp_metadata):
    xmp_metadata.subject = ""
    assert xmp_metadata.subject is None
    xml = xmp_metadata.to_string()
    assert "<dc:subject" not in xml


def test_instructions_setter(xmp_metadata):
    xmp_metadata.instructions = "Handle with care."
    assert xmp_metadata.instructions == "Handle with care."
    xml = xmp_metadata.to_string()
    assert "<photoshop:Instructions" in xml
    assert "Handle with care." in xml


def test_instructions_setter_invalid_data(xmp_metadata):
    with pytest.raises(TypeError):
        xmp_metadata.instructions = 12345


def test_instructions_setter_empty_string(xmp_metadata):
    xmp_metadata.instructions = ""
    assert xmp_metadata.instructions is None
    xml = xmp_metadata.to_string()
    assert "<photoshop:Instructions" not in xml


def test_to_wrapped_string(xmp_metadata):
    wrapped_xml = xmp_metadata.to_wrapped_string()
    assert wrapped_xml.startswith("<?xpacket begin=")
    assert wrapped_xml.endswith('<?xpacket end="w"?>')


def test_from_string():
    sample_xml = """<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>
    <x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">
        <rdf:RDF>
            <rdf:Description rdf:about="">
                <dc:creator>
                    <rdf:Seq>
                        <rdf:li>Alice</rdf:li>
                        <rdf:li>Bob</rdf:li>
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
                <dc:subject>
                    <rdf:Seq>
                        <rdf:li>Keyword1</rdf:li>
                        <rdf:li>Keyword2</rdf:li>
                    </rdf:Seq>
                </dc:subject>
                <photoshop:Instructions>Handle with care.</photoshop:Instructions>
            </rdf:Description>
        </rdf:RDF>
    </x:xmpmeta>
    <?xpacket end="w"?>"""

    instance = JHXMPMetadata.from_string(sample_xml)
    assert instance.creator == "Alice, Bob"
    assert instance.title == "Sample Title"
    assert instance.description == "Sample Description"
    assert instance.subject == "Keyword1, Keyword2"
    assert instance.instructions == "Handle with care."


def test_namespace_consistency(xmp_metadata):
    xml = xmp_metadata.to_string()
    assert 'xmlns:dc="http://purl.org/dc/elements/1.1/"' in xml
    assert 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"' in xml
    assert 'xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"' in xml


def test_roundtrip_conversion(xmp_metadata):
    xmp_metadata.creator = "Alice, Bob"
    xmp_metadata.title = "Sample Title"
    xmp_metadata.description = "Sample Description"
    xmp_metadata.subject = "Keyword1, Keyword2"
    xmp_metadata.instructions = "Handle with care."

    xml = xmp_metadata.to_string()
    new_instance = JHXMPMetadata.from_string(xml)

    assert new_instance.creator == "Alice, Bob"
    assert new_instance.title == "Sample Title"
    assert new_instance.description == "Sample Description"
    assert new_instance.subject == "Keyword1, Keyword2"
    assert new_instance.instructions == "Handle with care."


def test_from_string_with_invalid_xml():
    invalid_xml = """<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>
    <x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:RDF>
            <rdf:Description rdf:about="">
                <dc:creator>
                    <rdf:Seq>
                        <rdf:li>Alice</rdf:li>
                        <rdf:li>Bob</rdf:li>
                    </rdf:Seq>
                </dc:creator>
                <dc:title>
                    <rdf:Alt>
                        <rdf:li>Sample Title</rdf:li>
                    </rdf:Alt>
                </dc:title>
                <!-- Missing closing tags here -->
    </x:xmpmeta>
    <?xpacket end="w"?>"""

    with pytest.raises(etree.XMLSyntaxError):
        JHXMPMetadata.from_string(invalid_xml)


def test_large_input_handling(xmp_metadata):
    large_creator = ", ".join(f"Author{i}" for i in range(1000))  # 1000 authors
    large_subject = ", ".join(f"Keyword{i}" for i in range(1000))  # 1000 keywords

    xmp_metadata.creator = large_creator
    xmp_metadata.subject = large_subject

    assert xmp_metadata.creator == large_creator
    assert xmp_metadata.subject == large_subject

    xml = xmp_metadata.to_string()
    assert xml.count("<rdf:li") == 2000  # 1000 for creator + 1000 for subject
