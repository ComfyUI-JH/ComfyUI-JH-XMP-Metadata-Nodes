from enum import StrEnum
from typing import NotRequired, Required, TypedDict


class JHNodeInputOutputTypeEnum(StrEnum):
    STRING = "STRING"
    IMAGE = "IMAGE"
    PROMPT = "PROMPT"
    EXTRA_PNGINFO = "EXTRA_PNGINFO"


JHNodeInputOutputType = JHNodeInputOutputTypeEnum | list[str]


class JHNodeInputOutputTypeOptions(TypedDict, total=False):
    tooltip: str
    default: str
    forceInput: bool


class JHInputTypesType(TypedDict, total=False):
    required: Required[
        dict[str, tuple[JHNodeInputOutputType, JHNodeInputOutputTypeOptions]]
    ]
    optional: NotRequired[
        dict[str, tuple[JHNodeInputOutputType, JHNodeInputOutputTypeOptions]]
    ]
    hidden: NotRequired[dict[str, JHNodeInputOutputType]]
