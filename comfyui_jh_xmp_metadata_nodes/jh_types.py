from enum import StrEnum
from typing import NotRequired, Required, TypedDict


class JHNodeInputOutputTypeEnum(StrEnum):
    STRING = "STRING"
    IMAGE = "IMAGE"
    PROMPT = "PROMPT"
    EXTRA_PNGINFO = "EXTRA_PNGINFO"


JHTypesNodeInputOutputType = JHNodeInputOutputTypeEnum | list[str]


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
