# The following hack is copyright pythongosssss
# https://github.com/pythongosssss/ComfyUI-Custom-Scripts
# ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
any = AnyType("*")
# ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑


class JHGetWidgetValueNode:
    """
    Get the value of a specific widget from the graph. This class is slightly fragile
    because it peeks into the inner data structure of the graph directly rather than
    through any kind of API. Any change in how the graph is stored could break this.

    Args:
        any_input: A raw link to any node in the graph.
        widget_name: The name of the widget to get the value of.
        prompt: The prompt dictionary from the graph.

    Returns:
        The value of the specified widget.

    Raises:
        ValueError: If widget_name is empty.
    """

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any_input": (any, {"rawLink": True}),
                "widget_name": ("STRING", {"multiline": False}),
            },
            "hidden": {
                "prompt": "PROMPT",
            },
        }

    RETURN_TYPES = ("PRIMITIVE",)
    FUNCTION = "get_widget_value"
    CATEGORY = "XMP Metadata Nodes"

    def get_widget_value(
        self,
        any_input,
        widget_name,
        prompt,
    ):
        if widget_name == "":
            raise ValueError("widget_name must not be empty")

        upstream_node_id = int(any_input[0])

        try:
            widget_value = prompt[str(upstream_node_id)]["inputs"][widget_name]
        except KeyError:
            raise KeyError(f"Widget {widget_name} not found in node {upstream_node_id}")

        return (widget_value,)
