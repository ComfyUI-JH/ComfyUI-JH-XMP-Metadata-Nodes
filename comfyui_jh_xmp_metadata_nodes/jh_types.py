"""
This module was heavily inspired, let's say, by the ComfyUI `node_typing` module.

https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/comfy_types/node_typing.py

Although no code was copied, the structure and the idea of the module was taken from
ComfyUI. Used by permission under the terms of the GPL.

Note that this module is not intended to be comprehensive. It only includes the data
types used in this project. Refer to the link above for a more complete implementation.
"""

from enum import StrEnum
from typing import NotRequired, Required, TypedDict


class JHAnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class JHNodeInputOutputTypeEnum(StrEnum):
    STRING = "STRING"
    INT = "INT"
    FLOAT = "FLOAT"

    PRIMITIVE = "STRING,FLOAT,INT,BOOLEAN"

    IMAGE = "IMAGE"
    MASK = "MASK"

    PROMPT = "PROMPT"
    EXTRA_PNGINFO = "EXTRA_PNGINFO"

    ANY = JHAnyType("*")


JHTypesNodeInputOutputType = JHNodeInputOutputTypeEnum | JHAnyType | list[str]


class JHNodeInputOutputTypeOptions(TypedDict, total=False):
    tooltip: str
    default: str
    placeholder: str
    multiline: bool
    dynamicPrompts: bool

    min: int | float
    max: int | float
    step: int | float

    defaultInput: bool
    forceInput: bool
    lazy: bool

    label_on: str
    label_off: str

    rawLink: bool
    image_upload: bool


class JHInputTypesType(TypedDict, total=False):
    required: Required[
        dict[str, tuple[JHTypesNodeInputOutputType, JHNodeInputOutputTypeOptions]]
    ]
    optional: NotRequired[
        dict[str, tuple[JHTypesNodeInputOutputType, JHNodeInputOutputTypeOptions]]
    ]
    hidden: NotRequired[dict[str, str]]
