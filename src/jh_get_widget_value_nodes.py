"""
jh_get_widget_value_nodes

This module provides utility nodes for retrieving the value of specific widgets
from a graph structure in ComfyUI. These nodes are designed to work with the
XMP Metadata Nodes extension, offering support for extracting values in
different types (string, integer, float, or primitive).

Classes:
    - JHGetWidgetValueNode: Base class for extracting a widget value.
    - JHGetWidgetValueStringNode: Extracts widget values as strings.
    - JHGetWidgetValueIntNode: Extracts widget values as integers.
    - JHGetWidgetValueFloatNode: Extracts widget values as floats.

These nodes operate by peeking into the graph's internal data structure
to access widget inputs. While functional, they are somewhat fragile
and may break if the graph's internal representation changes.

"""

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
    def IS_CHANGED(
        cls, *args, **kwargs
    ):  # pylint: disable=invalid-name,unused-argument
        """
        Determines whether the node's output should be re-evaluated.

        Always returns True, regardless of the arguments passed, ensuring that
        the node reprocesses its inputs on every execution.

        Args:
            *args: Positional arguments passed dynamically by the framework.
            **kwargs: Keyword arguments passed dynamically by the framework.

        Returns:
            bool: Always True.
        """
        return True

    @classmethod
    def INPUT_TYPES(cls):  # pylint: disable=invalid-name
        """
        Defines the input types required by the node.

        Specifies the inputs that the node accepts, including any raw links to
        other nodes, the name of the widget to retrieve the value from, and
        the prompt dictionary.

        Returns:
            dict: A dictionary describing required and hidden inputs.
        """
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

    def get_widget_value(self, any_input, widget_name, prompt):
        """
        Retrieves the value of a specified widget from the graph.

        Args:
            any_input (tuple): A raw link to another node in the graph.
            widget_name (str): The name of the widget to fetch the value for.
            prompt (dict): The prompt dictionary representing the graph.

        Returns:
            tuple: A single-item tuple containing the widget's value.

        Raises:
            ValueError: If the widget name is empty.
            KeyError: If the widget or upstream node ID is not found.
        """
        if widget_name == "":
            raise ValueError("widget_name must not be empty")

        upstream_node_id = int(any_input[0])
        widget_value = self._get_widget_value_from_graph(
            upstream_node_id, widget_name, prompt
        )
        return (widget_value,)

    @staticmethod
    def _get_widget_value_from_graph(node_id, widget_name, graph_data):
        """
        Retrieves the value of a widget from the graph's internal data structure.

        This method abstracts the logic for accessing the graph's internals,
        making it easier to update if the structure changes in future versions
        of ComfyUI. The way it's written right now is basically magic, and will
        break if Comfy changes the graph data structure(s) basically at all. Here's
        hoping they stay as they are.

        Args:
            node_id (int): The ID of the upstream node.
            widget_name (str): The name of the widget to fetch the value for.
            graph_data (dict): The graph's prompt dictionary.

        Returns:
            The value of the widget.

        Raises:
            KeyError: If the node ID or widget name is not found in the graph.
        """
        try:
            return graph_data[str(node_id)]["inputs"][widget_name]
        except KeyError as exc:
            raise KeyError(
                f"Failed to retrieve widget '{widget_name}' from node {node_id}."
                " This may indicate a graph structure change or invalid input."
            ) from exc


class JHGetWidgetValueStringNode(JHGetWidgetValueNode):
    """
    A node that retrieves a widget's value as a string.

    Inherits from `JHGetWidgetValueNode` and converts the retrieved value
    to a string before returning it.

    Args:
        any_input (tuple): A raw link to another node in the graph.
        widget_name (str): The name of the widget to fetch the value for.
        prompt (dict): The prompt dictionary representing the graph.

    Returns:
        tuple: A single-item tuple containing the widget's value as a string.
    """

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
    """
    A node that retrieves a widget's value as an integer.

    Inherits from `JHGetWidgetValueNode` and converts the retrieved value
    to an integer before returning it. Raises a `ValueError` if the value
    cannot be converted to an integer.

    Args:
        any_input (tuple): A raw link to another node in the graph.
        widget_name (str): The name of the widget to fetch the value for.
        prompt (dict): The prompt dictionary representing the graph.

    Returns:
        tuple: A single-item tuple containing the widget's value as an integer.

    Raises:
        ValueError: If the widget's value cannot be converted to an integer.
    """

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
        except ValueError as exc:
            raise ValueError(f"""Widget "{widget_name}" is not an integer""") from exc
        return (widget_value,)


class JHGetWidgetValueFloatNode(JHGetWidgetValueNode):
    """
    A node that retrieves a widget's value as a float.

    Inherits from `JHGetWidgetValueNode` and converts the retrieved value
    to a float before returning it. Raises a `ValueError` if the value
    cannot be converted to a float.

    Args:
        any_input (tuple): A raw link to another node in the graph.
        widget_name (str): The name of the widget to fetch the value for.
        prompt (dict): The prompt dictionary representing the graph.

    Returns:
        tuple: A single-item tuple containing the widget's value as a float.

    Raises:
        ValueError: If the widget's value cannot be converted to a float.
    """

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
        except ValueError as exc:
            raise ValueError(f"""Widget "{widget_name}" is not a float""") from exc
        return (widget_value,)
