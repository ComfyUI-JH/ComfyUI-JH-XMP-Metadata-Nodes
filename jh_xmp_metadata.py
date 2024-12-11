import re
from typing import Optional

from lxml import etree


#
# https://developer.adobe.com/xmp/docs/XMPSpecifications/
#


class JHXMPMetadata:
    def __init__(self):
        self._creator: Optional[str] = None
        self._title: Optional[str] = None
        self._description: Optional[str] = None
        self._subject: Optional[str] = None
        self._instructions: Optional[str] = None
        self._make: Optional[str] = None
        self._model: Optional[str] = None

        # Set up the empty XMP metadata tree. We will add (and remove) elements as needed.

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

        self._dc_creator_element = None
        self._dc_title_element = None
        self._dc_description_element = None
        self._dc_subject_element = None
        self._photoshop_instructions_element = None
        self._tiff_make_element = None
        self._tiff_model_element = None
    
    @property
    def creator(self) -> Optional[str]:
        return self._creator
    
    @creator.setter
    def creator(self, value: Optional[str]) -> None:
        if value is not None:
            self._creator = set(self._string_to_list(value))
        else:
            self._creator = None
        if self._creator is None:
            if self._dc_creator_element is not None:
                self._rdf_description.remove(self._dc_creator_element)
        else:
            self._dc_creator_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}creator"
            )
            _seq = etree.SubElement(
                self._dc_creator_element,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Seq",
            )
            for _creator in self._creator:
                _li = etree.SubElement(
                    _seq,
                    "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                    attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
                )
                _li.text = _creator

    @property
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._title = value
        if self._title is None:
            if self._dc_title_element is not None:
                self._rdf_description.remove(self._dc_title_element)
        else:
            self._dc_title_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}title"
            )
            _alt = etree.SubElement(
                self._dc_title_element,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Alt",
            )
            _li = etree.SubElement(
                _alt,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
            )
            _li.text = self._title

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value
        if self._description is None:
            if self._dc_description_element is not None:
                self._rdf_description.remove(self._dc_description_element)
        else:
            self._dc_description_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}description"
            )
            _alt = etree.SubElement(
                self._dc_description_element,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Seq",
            )
            _li = etree.SubElement(
                _alt,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
            )
            _li.text = self._description

    @property
    def subject(self) -> Optional[str]:
        return self._subject

    @subject.setter
    def subject(self, value: Optional[str]) -> None:
        if value is not None:
            self._subject = set(self._string_to_list(value))
        else:
            self._subject = None
        if self._subject is None:
            if self._dc_subject_element is not None:
                self._rdf_description.remove(self._dc_subject_element)
        else:
            self._dc_subject_element = etree.SubElement(
                self._rdf_description, "{http://purl.org/dc/elements/1.1/}subject"
            )
            _seq = etree.SubElement(
                self._dc_subject_element,
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Seq",
            )
            for _subject in self._subject:
                _li = etree.SubElement(
                    _seq,
                    "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                    attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"},
                )
                _li.text = _subject

    @property
    def instructions(self) -> Optional[str]:
        return self._instructions

    @instructions.setter
    def instructions(self, value: Optional[str]) -> None:
        self._instructions = value
        if self._instructions is None:
            if self._photoshop_instructions_element is not None:
                self._rdf_description.remove(self._photoshop_instructions_element)
        else:
            self._photoshop_instructions_element = etree.SubElement(
                self._rdf_description,
                "{http://ns.adobe.com/photoshop/1.0/}Instructions",
            )
            self._photoshop_instructions_element.text = self._instructions

    @property
    def make(self) -> Optional[str]:
        return self._make

    @make.setter
    def make(self, value: Optional[str]) -> None:
        self._make = value
        if self._make is None:
            if self._tiff_make_element is not None:
                self._rdf_description.remove(self._tiff_make_element)
        else:
            self._tiff_make_element = etree.SubElement(
                self._rdf_description, "{http://ns.adobe.com/tiff/1.0/}Make"
            )
            self._tiff_make_element.text = self._make

    @property
    def model(self) -> Optional[str]:
        return self._model

    @model.setter
    def model(self, value: Optional[str]) -> None:
        self._model = value
        if self._model is None:
            if self._tiff_model_element is not None:
                self._rdf_description.remove(self._tiff_model_element)
        else:
            self._tiff_model_element = etree.SubElement(
                self._rdf_description, "{http://ns.adobe.com/tiff/1.0/}Model"
            )
            self._tiff_model_element.text = self._model

    def _string_to_list(self, string):
        return re.split(r"[;,]\s*", string)

    def to_string(self, pretty_print=False) -> Optional[str]:
        return etree.tostring(
            self._xmpmetadata, pretty_print=pretty_print, encoding="UTF-8"
        ).decode("utf-8")

    def to_wrapped_string(self) -> Optional[str]:
        return f"""<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>{self.to_string()}<?xpacket end="w"?>"""
