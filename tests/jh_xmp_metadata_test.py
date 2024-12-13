import textwrap

from lxml import etree
import pytest

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
    metadata = JHXMPMetadata.from_string(xml_string)
    assert metadata.creator == "John Doe, Jane Doe"
    assert metadata.title == "Test Title"
    assert metadata.description == "Test Description"
    assert metadata.subject == "Subject 1, Subject 2"
    assert metadata.instructions == "Test Instructions"


def test_from_string_different_xml():
    xml_string = textwrap.dedent(
        """
        <?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>
        <x:xmpmeta
            xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 6.0.0">
            <rdf:RDF
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
                <rdf:Description rdf:about=""
                    xmlns:exif="http://ns.adobe.com/exif/1.0/"
                    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
                    xmlns:tiff="http://ns.adobe.com/tiff/1.0/"
                    xmlns:exifEX="http://cipa.jp/exif/1.0/"
                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">
                    <exif:CompositeImage>2</exif:CompositeImage>
                    <exif:WhiteBalance>0</exif:WhiteBalance>
                    <exif:ExposureMode>0</exif:ExposureMode>
                    <exif:PixelYDimension>4284</exif:PixelYDimension>
                    <exif:ISOSpeedRatings>
                        <rdf:Seq>
                            <rdf:li>80</rdf:li>
                        </rdf:Seq>
                    </exif:ISOSpeedRatings>
                    <exif:GPSLatitude>44,0.230667N</exif:GPSLatitude>
                    <exif:GPSLongitude>83,3.76883W</exif:GPSLongitude>
                    <exif:ColorSpace>65535</exif:ColorSpace>
                    <exif:GPSTimeStamp>2024-07-04T18:55:19</exif:GPSTimeStamp>
                    <exif:GPSDestBearingRef>T</exif:GPSDestBearingRef>
                    <exif:GPSImgDirection>313097/1224</exif:GPSImgDirection>
                    <exif:ApertureValue>42657/25639</exif:ApertureValue>
                    <exif:GPSAltitudeRef>0</exif:GPSAltitudeRef>
                    <exif:SubsecTimeOriginal>067</exif:SubsecTimeOriginal>
                    <exif:GPSImgDirectionRef>T</exif:GPSImgDirectionRef>
                    <exif:ExposureTime>1/6410</exif:ExposureTime>
                    <exif:GPSLongitudeRef>W</exif:GPSLongitudeRef>
                    <exif:BrightnessValue>139383/13619</exif:BrightnessValue>
                    <exif:FocalLength>251773/37217</exif:FocalLength>
                    <exif:GPSDestBearing>313097/1224</exif:GPSDestBearing>
                    <exif:SubjectArea>
                        <rdf:Seq>
                            <rdf:li>2846</rdf:li>
                            <rdf:li>2133</rdf:li>
                            <rdf:li>3129</rdf:li>
                            <rdf:li>1876</rdf:li>
                        </rdf:Seq>
                    </exif:SubjectArea>
                    <exif:OffsetTime>-04:00</exif:OffsetTime>
                    <exif:ShutterSpeedValue>46677/3691</exif:ShutterSpeedValue>
                    <exif:SubsecTimeDigitized>067</exif:SubsecTimeDigitized>
                    <exif:GPSLatitudeRef>N</exif:GPSLatitudeRef>
                    <exif:FNumber>1244236/699009</exif:FNumber>
                    <exif:ExposureProgram>2</exif:ExposureProgram>
                    <exif:GPSSpeed>9549/29020</exif:GPSSpeed>
                    <exif:SensingMethod>2</exif:SensingMethod>
                    <exif:OffsetTimeDigitized>-04:00</exif:OffsetTimeDigitized>
                    <exif:MeteringMode>5</exif:MeteringMode>
                    <exif:GPSAltitude>238535/1327</exif:GPSAltitude>
                    <exif:SceneType>1</exif:SceneType>
                    <exif:Flash rdf:parseType="Resource">
                        <exif:Function>False</exif:Function>
                        <exif:Fired>False</exif:Fired>
                        <exif:Return>0</exif:Return>
                        <exif:Mode>2</exif:Mode>
                        <exif:RedEyeMode>False</exif:RedEyeMode>
                    </exif:Flash>
                    <exif:OffsetTimeOriginal>-04:00</exif:OffsetTimeOriginal>
                    <exif:GPSHPositioningError>91689/6083</exif:GPSHPositioningError>
                    <exif:GPSSpeedRef>K</exif:GPSSpeedRef>
                    <exif:ExposureBiasValue>0</exif:ExposureBiasValue>
                    <exif:PixelXDimension>5712</exif:PixelXDimension>
                    <exif:FocalLenIn35mmFilm>24</exif:FocalLenIn35mmFilm>
                    <exif:ExifVersion>0232</exif:ExifVersion>
                    <exif:SubsecTime>067</exif:SubsecTime>
                    <xmp:ModifyDate>2024-07-04T14:55:20</xmp:ModifyDate>
                    <xmp:CreateDate>2024-07-04T14:55:20</xmp:CreateDate>
                    <xmp:CreatorTool>17.5.1</xmp:CreatorTool>
                    <tiff:Orientation>1</tiff:Orientation>
                    <tiff:XResolution>72</tiff:XResolution>
                    <tiff:HostComputer>iPhone 15 Pro</tiff:HostComputer>
                    <tiff:ResolutionUnit>2</tiff:ResolutionUnit>
                    <tiff:YResolution>72</tiff:YResolution>
                    <tiff:Make>Apple</tiff:Make>
                    <tiff:TileLength>896</tiff:TileLength>
                    <tiff:TileWidth>640</tiff:TileWidth>
                    <tiff:Model>iPhone 15 Pro</tiff:Model>
                    <exifEX:PhotographicSensitivity>80</exifEX:PhotographicSensitivity>
                    <exifEX:LensMake>Apple</exifEX:LensMake>
                    <exifEX:LensModel>iPhone 15 Pro back triple camera 6.765mm f/1.78</exifEX:LensModel>
                    <exifEX:LensSpecification>
                        <rdf:Seq>
                            <rdf:li>1551800/699009</rdf:li>
                            <rdf:li>9</rdf:li>
                            <rdf:li>1244236/699009</rdf:li>
                            <rdf:li>14/5</rdf:li>
                        </rdf:Seq>
                    </exifEX:LensSpecification>
                    <dc:subject>
                        <rdf:Bag/>
                    </dc:subject>
                    <photoshop:DateCreated>2024-07-04T14:55:20-04:00</photoshop:DateCreated>
                </rdf:Description>
            </rdf:RDF>
        </x:xmpmeta>
        <?xpacket end="w"?>
        """
    ).strip()
    metadata = JHXMPMetadata.from_string(xml_string)
    assert metadata.creator is None
    assert metadata.title is None
    assert metadata.description is None
    assert metadata.subject is None
    assert metadata.instructions is None


def test_from_string_invalid_xml():
    xml_string = textwrap.dedent(
        """
        foobar
        """
    ).strip()
    with pytest.raises(etree.XMLSyntaxError):
        metadata = JHXMPMetadata.from_string(xml_string)
        assert metadata is None
