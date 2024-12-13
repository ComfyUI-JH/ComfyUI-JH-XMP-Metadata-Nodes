from .any_type import AnyType

any_type = AnyType("*")


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
                "any_input": (any_type, {"rawLink": True}),
                "widget_name": ("STRING", {"multiline": False}),
            },
            "hidden": {
                "prompt": "PROMPT",
            },
        }

    RETURN_TYPES = ("PRIMITIVE",)
    OUTPUT_NODE = False
    FUNCTION = "get_widget_value"
    CATEGORY = "XMP Metadata Nodes/Utilities"

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


class JHGetWidgetValueStringNode(JHGetWidgetValueNode):
    RETURN_TYPES = ("STRING",)

    def get_widget_value(
        self,
        any_input,
        widget_name,
        prompt,
    ):
        widget_value = str(super().get_widget_value(any_input, widget_name, prompt)[0])
        return (widget_value,)


class JHGetWidgetValueIntNode(JHGetWidgetValueNode):
    RETURN_TYPES = ("INT",)

    def get_widget_value(
        self,
        any_input,
        widget_name,
        prompt,
    ):
        widget_value = None
        try:
            widget_value = int(
                super().get_widget_value(any_input, widget_name, prompt)[0]
            )
        except ValueError:
            raise ValueError(f"""Widget "{widget_name}" is not an integer""")
        return (widget_value,)


class JHGetWidgetValueFloatNode(JHGetWidgetValueNode):
    RETURN_TYPES = ("FLOAT",)

    def get_widget_value(
        self,
        any_input,
        widget_name,
        prompt,
    ):
        widget_value = None
        try:
            widget_value = float(
                super().get_widget_value(any_input, widget_name, prompt)[0]
            )
        except ValueError:
            raise ValueError(f"""Widget "{widget_name}" is not a float""")
        return (widget_value,)
