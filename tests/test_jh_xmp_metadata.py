import textwrap
from dataclasses import dataclass

import pytest
from lxml import etree

from comfyui_jh_xmp_metadata_nodes.jh_xmp_metadata import JHXMPMetadata

# region Type Definitions


@dataclass
class MetadataDataclass:
    creator: str | None
    rights: str | None
    title: str | None
    description: str | None
    subject: str | None
    instructions: str | None
    comment: str | None
    alt_text: str | None
    ext_description: str | None


# endregion Type Definitions

# region Fixtures


@pytest.fixture
def sample_metadata() -> MetadataDataclass:
    metadata = MetadataDataclass(
        creator="John Doe",
        rights="© 2020 John Doe",
        title="My Title",
        description="My Description",
        subject="subject1, subject2",
        instructions="My Instructions",
        comment="My Comment",
        alt_text="My Alt Text",
        ext_description="My Extended Description",
    )
    return metadata


@pytest.fixture
def empty_metadata() -> MetadataDataclass:
    metadata = MetadataDataclass(
        creator=None,
        rights=None,
        title=None,
        description=None,
        subject=None,
        instructions=None,
        comment=None,
        alt_text=None,
        ext_description=None,
    )
    return metadata


@pytest.fixture
def valid_xml_string(sample_metadata: MetadataDataclass) -> str:
    return textwrap.dedent(f"""
        <x:xmpmeta
            xmlns:x="adobe:ns:meta/"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/" x:xmptk="Adobe XMP Core 6.0-c002 79.164861, 2016/09/14-01:09:01">
            <rdf:RDF>
                <rdf:Description rdf:about="">
                    <dc:creator>
                        <rdf:Seq>
                            <rdf:li xml:lang="x-default">{sample_metadata.creator}</rdf:li>
                        </rdf:Seq>
                    </dc:creator>
                    <dc:rights>
                        <rdf:Alt>
                            <rdf:li xml:lang="x-default">{sample_metadata.rights}</rdf:li>
                        </rdf:Alt>
                    </dc:rights>
                    <dc:title>
                        <rdf:Alt>
                            <rdf:li xml:lang="x-default">{sample_metadata.title}</rdf:li>
                        </rdf:Alt>
                    </dc:title>
                    <dc:description>
                        <rdf:Alt>
                            <rdf:li xml:lang="x-default">{sample_metadata.description}</rdf:li>
                        </rdf:Alt>
                    </dc:description>
                    <dc:subject>
                        <rdf:Bag>
                            <rdf:li xml:lang="x-default">{str(sample_metadata.subject).split(", ")[0]}</rdf:li>
                            <rdf:li xml:lang="x-default">{str(sample_metadata.subject).split(", ")[1]}</rdf:li>
                        </rdf:Bag>
                    </dc:subject>
                    <photoshop:Instructions>{sample_metadata.instructions}</photoshop:Instructions>
                    <exif:UserComment>
                        <rdf:Alt>
                            <rdf:li xml:lang="x-default">{sample_metadata.comment}</rdf:li>
                        </rdf:Alt>
                    </exif:UserComment>
                    <Iptc4xmpCore:AltTextAccessibility>{sample_metadata.alt_text}</Iptc4xmpCore:AltTextAccessibility>
                    <Iptc4xmpCore:ExtDescrAccessibility>{sample_metadata.ext_description}</Iptc4xmpCore:ExtDescrAccessibility>
                </rdf:Description>
            </rdf:RDF>
        </x:xmpmeta>
        """).strip()  # noqa: E501


@pytest.fixture
def incomplete_xml_string(sample_metadata: MetadataDataclass) -> str:
    return textwrap.dedent(f"""
        <x:xmpmeta
            xmlns:x="adobe:ns:meta/"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/" x:xmptk="Adobe XMP Core 6.0-c002 79.164861, 2016/09/14-01:09:01">
            <rdf:RDF>
                <rdf:Description rdf:about="">
                    <dc:creator>
                        <rdf:Seq>
                            <rdf:li xml:lang="x-default">{sample_metadata.creator}</rdf:li>
                        </rdf:Seq>
                    </dc:creator>
                    <dc:rights>
                        <rdf:Alt>
                            <rdf:li xml:lang="x-default">{sample_metadata.rights}</rdf:li>
                        </rdf:Alt>
                    </dc:rights>
                </rdf:Description>
            </rdf:RDF>
        </x:xmpmeta>
        """).strip()  # noqa: E501


@pytest.fixture
def invalid_xml_string() -> str:
    return "This is not valid XML."


@pytest.fixture
def empty_metadata_object() -> JHXMPMetadata:
    return JHXMPMetadata()


@pytest.fixture
def sample_metadata_object(sample_metadata: MetadataDataclass) -> JHXMPMetadata:
    metadata = JHXMPMetadata()
    metadata.creator = sample_metadata.creator
    metadata.rights = sample_metadata.rights
    metadata.title = sample_metadata.title
    metadata.description = sample_metadata.description
    metadata.subject = sample_metadata.subject
    metadata.instructions = sample_metadata.instructions
    metadata.comment = sample_metadata.comment
    metadata.alt_text = sample_metadata.alt_text
    metadata.ext_description = sample_metadata.ext_description
    return metadata


# endregion Fixtures


def test_initialization(empty_metadata_object: JHXMPMetadata) -> None:
    assert empty_metadata_object.creator is None
    assert empty_metadata_object.rights is None
    assert empty_metadata_object.title is None
    assert empty_metadata_object.description is None
    assert empty_metadata_object.subject is None
    assert empty_metadata_object.instructions is None
    assert empty_metadata_object.comment is None
    assert empty_metadata_object.alt_text is None
    assert empty_metadata_object.ext_description is None


def test_from_string(valid_xml_string: str, sample_metadata: MetadataDataclass) -> None:
    metadata = JHXMPMetadata.from_string(valid_xml_string)
    assert metadata.creator == sample_metadata.creator
    assert metadata.rights == sample_metadata.rights
    assert metadata.title == sample_metadata.title
    assert metadata.description == sample_metadata.description
    assert metadata.subject == sample_metadata.subject
    assert metadata.instructions == sample_metadata.instructions
    assert metadata.comment == sample_metadata.comment
    assert metadata.alt_text == sample_metadata.alt_text
    assert metadata.ext_description == sample_metadata.ext_description


def test_from_string_with_incomplete_xml(
    incomplete_xml_string: str, sample_metadata: MetadataDataclass
) -> None:
    metadata = JHXMPMetadata.from_string(incomplete_xml_string)
    assert metadata.creator == sample_metadata.creator
    assert metadata.rights == sample_metadata.rights
    assert metadata.title is None
    assert metadata.description is None
    assert metadata.subject is None
    assert metadata.instructions is None
    assert metadata.comment is None
    assert metadata.alt_text is None
    assert metadata.ext_description is None


def test_from_string_with_invalid_xml(invalid_xml_string: str) -> None:
    metadata = JHXMPMetadata.from_string(invalid_xml_string)
    assert metadata.creator is None
    assert metadata.rights is None
    assert metadata.title is None
    assert metadata.description is None
    assert metadata.subject is None
    assert metadata.instructions is None
    assert metadata.comment is None
    assert metadata.alt_text is None
    assert metadata.ext_description is None


def test_property_creator(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.creator = sample_metadata.creator
    assert empty_metadata_object.creator == sample_metadata.creator
    empty_metadata_object.creator = None
    assert empty_metadata_object.creator is None


def test_property_rights(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.rights = sample_metadata.rights
    assert empty_metadata_object.rights == sample_metadata.rights
    empty_metadata_object.rights = None
    assert empty_metadata_object.rights is None


def test_property_title(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.title = sample_metadata.title
    assert empty_metadata_object.title == sample_metadata.title
    empty_metadata_object.title = None
    assert empty_metadata_object.title is None


def test_property_description(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.description = sample_metadata.description
    assert empty_metadata_object.description == sample_metadata.description
    empty_metadata_object.description = None
    assert empty_metadata_object.description is None


def test_property_subject(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.subject = sample_metadata.subject
    assert empty_metadata_object.subject == sample_metadata.subject
    empty_metadata_object.subject = None
    assert empty_metadata_object.subject is None


def test_property_instructions(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.instructions = sample_metadata.instructions
    assert empty_metadata_object.instructions == sample_metadata.instructions
    empty_metadata_object.instructions = None
    assert empty_metadata_object.instructions is None


def test_property_comment(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.comment = sample_metadata.comment
    assert empty_metadata_object.comment == sample_metadata.comment
    empty_metadata_object.comment = None
    assert empty_metadata_object.comment is None


def test_property_alt_text(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.alt_text = sample_metadata.alt_text
    assert empty_metadata_object.alt_text == sample_metadata.alt_text
    empty_metadata_object.alt_text = None
    assert empty_metadata_object.alt_text is None


def test_property_ext_description(
    empty_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    empty_metadata_object.ext_description = sample_metadata.ext_description
    assert empty_metadata_object.ext_description == sample_metadata.ext_description
    empty_metadata_object.ext_description = None
    assert empty_metadata_object.ext_description is None


def validate_xml_string(xml_string: str, metadata_object: MetadataDataclass) -> None:
    root = etree.fromstring(xml_string, parser=etree.XMLParser())
    rdf_description = root.xpath(
        "/x:xmpmeta/rdf:RDF/rdf:Description", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(rdf_description) == 1

    creator_element = rdf_description[0].xpath(
        "./dc:creator",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(creator_element) == 1
    li_elements = creator_element[0].xpath(
        "./rdf:Seq/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(li_elements) == 1 and li_elements[0].text == metadata_object.creator
    rdf_description[0].remove(creator_element[0])

    rights_element = rdf_description[0].xpath(
        "./dc:rights",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(rights_element) == 1
    li_elements = rights_element[0].xpath(
        "./rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(li_elements) == 1 and li_elements[0].text == metadata_object.rights
    rdf_description[0].remove(rights_element[0])

    title_element = rdf_description[0].xpath(
        "./dc:title",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(title_element) == 1
    li_elements = title_element[0].xpath(
        "./rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(li_elements) == 1 and li_elements[0].text == metadata_object.title
    rdf_description[0].remove(title_element[0])

    description_element = rdf_description[0].xpath(
        "./dc:description",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(description_element) == 1
    li_elements = description_element[0].xpath(
        "./rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(li_elements) == 1 and li_elements[0].text == metadata_object.description
    rdf_description[0].remove(description_element[0])

    subject_element = rdf_description[0].xpath(
        "./dc:subject",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(subject_element) == 1
    li_elements = subject_element[0].xpath(
        "./rdf:Bag/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(li_elements) == 2
    assert ", ".join([li.text for li in li_elements]) == metadata_object.subject
    rdf_description[0].remove(subject_element[0])

    instructions_element = rdf_description[0].xpath(
        "./photoshop:Instructions",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(instructions_element) == 1
    assert instructions_element[0].text == metadata_object.instructions
    rdf_description[0].remove(instructions_element[0])

    comment_element = rdf_description[0].xpath(
        "./exif:UserComment",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(comment_element) == 1
    li_elements = comment_element[0].xpath(
        "./rdf:Alt/rdf:li", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(li_elements) == 1 and li_elements[0].text == metadata_object.comment
    rdf_description[0].remove(comment_element[0])

    alt_text_element = rdf_description[0].xpath(
        "./Iptc4xmpCore:AltTextAccessibility",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(alt_text_element) == 1
    assert alt_text_element[0].text == metadata_object.alt_text
    rdf_description[0].remove(alt_text_element[0])

    ext_description_element = rdf_description[0].xpath(
        "./Iptc4xmpCore:ExtDescrAccessibility",
        namespaces=JHXMPMetadata.NAMESPACES,
    )
    assert len(ext_description_element) == 1
    assert ext_description_element[0].text == metadata_object.ext_description
    rdf_description[0].remove(ext_description_element[0])

    children = rdf_description[0].getchildren()
    assert len(children) == 0


def test_to_string(
    sample_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    validate_xml_string(sample_metadata_object.to_string(), sample_metadata)


def test_to_string_with_empty_metadata(
    empty_metadata_object: JHXMPMetadata, empty_metadata: MetadataDataclass
) -> None:
    root = etree.fromstring(empty_metadata_object.to_string(), parser=etree.XMLParser())
    rdf_description = root.xpath(
        "/x:xmpmeta/rdf:RDF/rdf:Description", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(rdf_description) == 1
    children = rdf_description[0].getchildren()
    assert len(children) == 0


def test_to_wrapped_string(
    sample_metadata_object: JHXMPMetadata, sample_metadata: MetadataDataclass
) -> None:
    wrapped_string = sample_metadata_object.to_wrapped_string()
    assert wrapped_string.startswith(
        """<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>"""
    )
    assert wrapped_string.endswith("""<?xpacket end="w"?>""")
    validate_xml_string(wrapped_string, sample_metadata)


def test_to_wrapped_string_with_empty_metadata(
    empty_metadata_object: JHXMPMetadata, empty_metadata: MetadataDataclass
) -> None:
    wrapped_string = empty_metadata_object.to_wrapped_string()
    assert wrapped_string.startswith(
        """<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>"""
    )
    assert wrapped_string.endswith("""<?xpacket end="w"?>""")
    root = etree.fromstring(wrapped_string, parser=etree.XMLParser())
    rdf_description = root.xpath(
        "/x:xmpmeta/rdf:RDF/rdf:Description", namespaces=JHXMPMetadata.NAMESPACES
    )
    assert len(rdf_description) == 1
    children = rdf_description[0].getchildren()
    assert len(children) == 0
