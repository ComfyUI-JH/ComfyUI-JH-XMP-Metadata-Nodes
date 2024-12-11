from lxml import etree
import re
from typing import Optional


class JHXMPMetadata:
    def __init__(self):
        self._title: Optional[str] = None
        self._description: Optional[str] = None
        self._subject: Optional[str] = None
        self._instructions: Optional[str] = None
        self._make: Optional[str] = None
        self._model: Optional[str] = None

        self._xmpmetadata: Optional[etree.Element] = None

    @property
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._title = value
        self.update_xmpmetadata()

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value
        self.update_xmpmetadata()

    @property
    def subject(self) -> Optional[str]:
        return self._subject

    @subject.setter
    def subject(self, value: Optional[str]) -> None:
        self._subject = value
        self.update_xmpmetadata()

    @property
    def instructions(self) -> Optional[str]:
        return self._instructions

    @instructions.setter
    def instructions(self, value: Optional[str]) -> None:
        self._instructions = value
        self.update_xmpmetadata()

    @property
    def make(self) -> Optional[str]:
        return self._make

    @make.setter
    def make(self, value: Optional[str]) -> None:
        self._make = value
        self.update_xmpmetadata()

    @property
    def model(self) -> Optional[str]:
        return self._model

    @model.setter
    def model(self, value: Optional[str]) -> None:
        self._model = value
        self.update_xmpmetadata()

    def _string_to_list(self, string):
        return re.split(r"[;,]\s*", string)

    def update_xmpmetadata(self) -> None:

        #
        # https://developer.adobe.com/xmp/docs/XMPSpecifications/
        #

        NAMESPACES = {
            "x": "adobe:ns:meta/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc": "http://purl.org/dc/elements/1.1/",
            "xml": "http://www.w3.org/XML/1998/namespace",
            "xmp": "http://ns.adobe.com/xap/1.0/",
            "photoshop": "http://ns.adobe.com/photoshop/1.0/",
            "exif": "http://ns.adobe.com/exif/1.0/",
            "tiff": "http://ns.adobe.com/tiff/1.0/",
        }

        self._xmpmetadata = etree.Element("{adobe:ns:meta/}xmpmeta", nsmap=NAMESPACES)
        self._xmpmetadata.set(
            "{adobe:ns:meta/}xmptk",
            "Adobe XMP Core 6.0-c002 79.164861, 2016/09/14-01:09:01",
        )
        self._rdf = etree.SubElement(
            self._xmpmetadata, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF"
        )
        self._rdf_description = etree.SubElement(
            self._rdf,
            "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description",
            attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": ""},
        )

        # title → dc:title
        if self._title:
            _dc_title_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}title"
            )
            _alt = etree.SubElement(
                _dc_title_element, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Alt"
            )
            _li = etree.SubElement(
                _alt,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
            )
            _li.text = self._title

        # description → dc:description
        if self._description:
            _dc_description_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}description"
            )
            _alt = etree.SubElement(
                _dc_description_element,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Alt",
            )
            _li = etree.SubElement(
                _alt,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
            )
            _li.text = self._description

        # subject → dc:subject
        if self._subject:
            _dc_subject_set = set(self._string_to_list(self._subject))
            _dc_subject_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}subject"
            )
            _seq = etree.SubElement(
                _dc_subject_element, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Seq"
            )
            for self._subject in _dc_subject_set:
                _li = etree.SubElement(
                    _seq,
                    "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                    attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
                )
                _li.text = self._subject

        # instructions → photoshop:Instructions
        if self._instructions:
            _photoshop_instructions_element = etree.SubElement(
                self._rdf_description,
                "{http://ns.adobe.com/photoshop/1.0/}Instructions",
            )
            _photoshop_instructions_element.text = self._instructions

        # make → tiff:Make
        if self._make:
            _tiff_make_element = etree.SubElement(
                self._rdf_description, "{http://ns.adobe.com/tiff/1.0/}Make"
            )
            _tiff_make_element.text = self._make

        # model → tiff:Model
        if self._model:
            _tiff_model_element = etree.SubElement(
                self._rdf_description, "{http://ns.adobe.com/tiff/1.0/}Model"
            )
            _tiff_model_element.text = self._model

    def to_string(self, pretty_print=False) -> Optional[str]:
        return etree.tostring(
            self._xmpmetadata, pretty_print=pretty_print, encoding="UTF-8"
        ).decode("utf-8")

    def to_wrapped_string(self) -> Optional[str]:
        return f"""<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>{self.to_string()}<?xpacket end="w"?>"""
