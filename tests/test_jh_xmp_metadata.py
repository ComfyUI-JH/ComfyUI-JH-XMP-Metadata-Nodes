import time

import pytest
from lxml import etree

from src.jh_xmp_metadata import JHXMPMetadata


@pytest.fixture
def xmp_metadata():
    return JHXMPMetadata()


# Test setters and basic functionality
class TestBasicFunctionality:
    def test_initial_state(self, xmp_metadata):
        assert xmp_metadata.creator is None
        assert xmp_metadata.title is None
        assert xmp_metadata.description is None
        assert xmp_metadata.subject is None
        assert xmp_metadata.instructions is None
        assert xmp_metadata.to_string() is not None

    @pytest.mark.parametrize(
        "field, value, expected_tag",
        [
            ("creator", "Alice, Bob", "<dc:creator"),
            ("title", "Sample Title", "<dc:title"),
            ("description", "Sample Description", "<dc:description"),
            ("subject", "Keyword1, Keyword2", "<dc:subject"),
            ("instructions", "Handle with care.", "<photoshop:Instructions"),
        ],
    )
    def test_setter(self, xmp_metadata, field, value, expected_tag):
        setattr(xmp_metadata, field, value)
        assert getattr(xmp_metadata, field) == value
        xml = xmp_metadata.to_string()
        assert expected_tag in xml
        assert value.split(", ")[0] in xml

    def test_whitespace_handling(self, xmp_metadata):
        xmp_metadata.title = "   "
        assert (
            xmp_metadata.title is None
        ), "Title should be None for whitespace-only input."
        xml = xmp_metadata.to_string()
        assert "<dc:title" not in xml, "Whitespace-only title should not appear in XML."

    def test_special_characters_in_metadata(self, xmp_metadata):
        xmp_metadata.creator = "Alice & Bob <Team>"
        xmp_metadata.title = "Title with > symbol"
        xmp_metadata.description = "Description with < and & symbols"
        xml = xmp_metadata.to_string()

        assert "&amp;" in xml, "Special character '&' was not properly escaped."
        assert "&lt;" in xml, "Special character '<' was not properly escaped."
        assert "&gt;" in xml, "Special character '>' was not properly escaped."

    def test_special_characters_extended(self, xmp_metadata):
        xmp_metadata.subject = "Emoji: 😊, Unicode: 你好"
        xml = xmp_metadata.to_string()

        assert "😊" in xml, "Emoji should appear as-is in XML."
        assert "你好" in xml, "Unicode characters should appear as-is in XML."


# Test serialization and roundtrip functionality
class TestSerialization:
    def test_to_wrapped_string(self, xmp_metadata):
        wrapped_xml = xmp_metadata.to_wrapped_string()
        assert wrapped_xml.startswith("<?xpacket begin=")
        assert wrapped_xml.endswith('<?xpacket end="w"?>')

    def test_namespace_consistency(self, xmp_metadata):
        xml = xmp_metadata.to_string()
        assert 'xmlns:dc="http://purl.org/dc/elements/1.1/"' in xml
        assert 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"' in xml
        assert 'xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"' in xml

    def test_roundtrip_conversion(self, xmp_metadata):
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

    def test_namespace_roundtrip(self, xmp_metadata):
        xmp_metadata.creator = "Alice, Bob"
        xml = xmp_metadata.to_string()
        new_instance = JHXMPMetadata.from_string(xml)
        assert 'xmlns:dc="http://purl.org/dc/elements/1.1/"' in new_instance.to_string()


# Test deserialization and parsing
class TestDeserialization:
    def test_from_string(self):
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

    def test_from_string_with_invalid_xml(self):
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

    def test_from_empty_string(self):
        with pytest.raises(etree.XMLSyntaxError):
            JHXMPMetadata.from_string("")
        with pytest.raises(etree.XMLSyntaxError):
            JHXMPMetadata.from_string("   ")

    def test_minimal_valid_xml(self):
        minimal_xml = """<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>
        <x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:RDF>
                <rdf:Description rdf:about="" />
            </rdf:RDF>
        </x:xmpmeta>
        <?xpacket end="w"?>"""

        instance = JHXMPMetadata.from_string(minimal_xml)
        assert instance.creator is None
        assert instance.title is None
        assert instance.description is None
        assert instance.subject is None
        assert instance.instructions is None


# Test performance and scalability
class TestPerformance:
    def test_large_input_handling(self, xmp_metadata):
        large_creator = ", ".join(f"Author{i}" for i in range(1000))
        large_subject = ", ".join(f"Keyword{i}" for i in range(1000))

        xmp_metadata.creator = large_creator
        xmp_metadata.subject = large_subject

        assert (
            xmp_metadata.creator == large_creator
        ), "Creator should handle 1000 entries."
        assert (
            xmp_metadata.subject == large_subject
        ), "Subject should handle 1000 entries."

        xml = xmp_metadata.to_string()
        assert (
            xml.count("<rdf:li") == 2000
        ), "Expected 2000 <rdf:li> elements in XML for large inputs."

    def test_large_xml_performance(self):
        large_creator_list = "".join(
            f"<rdf:li>Author {i}</rdf:li>" for i in range(5000)
        )
        large_subject_list = "".join(
            f"<rdf:li>Keyword {i}</rdf:li>" for i in range(5000)
        )
        large_xml = f"""<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>
        <x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:RDF>
                <rdf:Description rdf:about="">
                    <dc:creator>
                        <rdf:Seq>{large_creator_list}</rdf:Seq>
                    </dc:creator>
                    <dc:subject>
                        <rdf:Seq>{large_subject_list}</rdf:Seq>
                    </dc:subject>
                </rdf:Description>
            </rdf:RDF>
        </x:xmpmeta>
        <?xpacket end="w"?>"""

        start_time = time.time()
        instance = JHXMPMetadata.from_string(large_xml)
        elapsed_time = time.time() - start_time

        assert (
            len(instance.creator.split(", ")) == 5000
        ), "Creator should handle 5000 entries."
        assert (
            len(instance.subject.split(", ")) == 5000
        ), "Subject should handle 5000 entries."
        assert elapsed_time < 5, "Parsing should complete within 5 seconds."
