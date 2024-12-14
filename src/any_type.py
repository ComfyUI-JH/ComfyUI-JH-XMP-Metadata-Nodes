"""
This module defines a specialized string subclass, `AnyType`, which
overrides the inequality operator (`!=`) to always return `False`. This
behavior makes instances of `AnyType` appear equal to any value when
compared using `!=`.

Copyright:
    This code is authored by pythongosssss and licensed under the MIT
    License. https://github.com/pythongosssss/ComfyUI-Custom-Scripts
"""


class AnyType(str):
    """
    A specialized string subclass which overrides the inequality
    operator (`!=`) to always return `False`. This behavior makes
    instances of `AnyType` appear equal to any value when compared using
    `!=`.

    This class is meant for use with the `JHGetWidgetValueNode` and its
    derived classes, where it is used as a placeholder value for
    comparison against arbitrary values.

    Examples:
        >>> any_type = AnyType("*")
        >>> any_type != "hello"
        False
        >>> any_type != 123
        False
        >>> any_type != [1, 2, 3]
        False
    """

    def __ne__(self, __value: object) -> bool:
        """
        Always returns False, as any value is considered equal to
        AnyType.
        """
        return False
