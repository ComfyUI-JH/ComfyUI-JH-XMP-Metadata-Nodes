import textwrap
from lxml import etree

from src.jh_xmp_metadata import JHXMPMetadata


def test_init():
    metadata = JHXMPMetadata()
    assert metadata.creator is None
    assert metadata.title is None
    assert metadata.description is None
    assert metadata.subject is None
    assert metadata.instructions is None


def test_set_creator():
    expected_creator = "John Doe, Jane Doe"
    metadata = JHXMPMetadata()
    metadata.creator = expected_creator
    assert metadata.creator == expected_creator


def test_set_title():
    expected_title = "My Title"
    metadata = JHXMPMetadata()
    metadata.title = expected_title
    assert metadata._title == expected_title


def test_set_description():
    expected_description = "My Description"
    metadata = JHXMPMetadata()
    metadata._description = expected_description
    assert metadata._description == expected_description


def test_set_subject():
    expected_subject = "Subject 1, Subject 2"
    metadata = JHXMPMetadata()
    metadata.subject = expected_subject
    assert metadata._subject == expected_subject


def test_set_instructions():
    expected_instructions = "My Instructions"
    metadata = JHXMPMetadata()
    metadata.instructions = expected_instructions
    assert metadata._instructions == expected_instructions


def test_to_string():
    expected_creator = "John Doe, Jane Doe"
    expected_title = "My Title"
    expected_description = "My Description"
    expected_subject = "Subject 1, Subject 2"
    expected_instructions = "My Instructions"
    metadata = JHXMPMetadata()
    metadata.creator = expected_creator
    metadata.title = expected_title
    metadata.description = expected_description
    metadata.subject = expected_subject
    metadata.instructions = expected_instructions
    xml_string = metadata.to_string()

    assert xml_string.startswith("<x:xmpmeta")

    root = etree.fromstring(xml_string)

    creator_list = list()
    for creator in root.xpath(
        "//dc:creator/rdf:Seq/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    ):
        creator_list.append(creator.text)
    creator = ", ".join(creator_list)
    assert creator == expected_creator

    title = root.xpath(
        "//dc:title/rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )[0].text
    assert title == expected_title

    description = root.xpath(
        "//dc:description/rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )[0].text
    assert description == expected_description

    subject_list = list()
    for subject in root.xpath(
        "//dc:subject/rdf:Seq/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    ):
        subject_list.append(subject.text)
    subject = ", ".join(subject_list)
    assert subject == expected_subject

    instructions = root.xpath(
        "//photoshop:Instructions", namespaces=JHXMPMetadata.NAMESPACES
    )[0].text
    assert instructions == expected_instructions


def test_to_wrapped_string():
    expected_creator = "John Doe, Jane Doe"
    expected_title = "My Title"
    expected_description = "My Description"
    expected_subject = "Subject 1, Subject 2"
    expected_instructions = "My Instructions"
    metadata = JHXMPMetadata()
    metadata.creator = expected_creator
    metadata.title = expected_title
    metadata.description = expected_description
    metadata.subject = expected_subject
    metadata.instructions = expected_instructions
    wrapped_string = metadata.to_wrapped_string()

    assert wrapped_string.startswith("<?xpacket")

    root = etree.fromstring(wrapped_string)

    creator_list = list()
    for creator in root.xpath(
        "//dc:creator/rdf:Seq/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    ):
        creator_list.append(creator.text)
    creator = ", ".join(creator_list)
    assert creator == expected_creator

    title = root.xpath(
        "//dc:title/rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )[0].text
    assert title == "My Title"

    description = root.xpath(
        "//dc:description/rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )[0].text
    assert description == expected_description

    subject_list = list()
    for subject in root.xpath(
        "//dc:subject/rdf:Seq/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    ):
        subject_list.append(subject.text)
    subject = ", ".join(subject_list)
    assert subject == expected_subject

    instructions = root.xpath(
        "//photoshop:Instructions", namespaces=JHXMPMetadata.NAMESPACES
    )[0].text
    assert instructions == expected_instructions


def test_from_string():
    xml_string = textwrap.dedent(
        """
        <?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>
        <x:xmpmeta
            xmlns:x="adobe:ns:meta/"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            x:xmptk="Adobe XMP Core 6.0-c002 79.164861, 2016/09/14-01:09:01">
            <rdf:RDF>
                <rdf:Description rdf:about="">
                    <dc:creator>
                        <rdf:Seq>
                            <rdf:li xml:lang="x-default">John Doe</rdf:li>
                            <rdf:li xml:lang="x-default">Jane Doe</rdf:li>
                        </rdf:Seq>
                    </dc:creator>
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
                        <rdf:Seq>
                            <rdf:li xml:lang="x-default">Subject 1</rdf:li>
                            <rdf:li xml:lang="x-default">Subject 2</rdf:li>
                        </rdf:Seq>
                    </dc:subject>
                    <photoshop:Instructions>Test Instructions</photoshop:Instructions>
                </rdf:Description>
            </rdf:RDF>
        </x:xmpmeta>
        <?xpacket end="w"?>
        """
    ).strip()
    metadata = JHXMPMetadata()
    metadata.from_string(xml_string)
    assert metadata.creator == "John Doe, Jane Doe"
    assert metadata.title == "Test Title"
    assert metadata.description == "Test Description"
    assert metadata.subject == "Subject 1, Subject 2"
    assert metadata.instructions == "Test Instructions"
