from enum import StrEnum
from typing import NotRequired, Required, TypedDict


class JHAnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class JHNodeInputOutputTypeEnum(StrEnum):
    STRING = "STRING"
    IMAGE = "IMAGE"
    PROMPT = "PROMPT"
    EXTRA_PNGINFO = "EXTRA_PNGINFO"

    ANY = JHAnyType("*")


JHTypesNodeInputOutputType = JHNodeInputOutputTypeEnum | JHAnyType | list[str]


class JHNodeInputOutputTypeOptions(TypedDict, total=False):
    tooltip: str
    default: str
    forceInput: bool


class JHInputTypesType(TypedDict, total=False):
    required: Required[
        dict[str, tuple[JHTypesNodeInputOutputType, JHNodeInputOutputTypeOptions]]
    ]
    optional: NotRequired[
        dict[str, tuple[JHTypesNodeInputOutputType, JHNodeInputOutputTypeOptions]]
    ]
    hidden: NotRequired[dict[str, JHTypesNodeInputOutputType]]
