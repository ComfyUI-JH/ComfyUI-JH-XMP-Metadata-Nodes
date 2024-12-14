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
    Get the value of a specific widget from the graph. This class is slightly
    fragile because it peeks into the inner data structure of the graph directly
    rather than through any kind of API. Any change in how the graph is stored
    could break this.

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
        Retrieves the value of a widget from the graph's internal data
        structure.

        This method handles the tricky business of digging into the graph's
        internals, so if ComfyUI changes how the graph is structured in the
        future, you'll only need to fix it here. Right now, it's a bit of a hack
        (okay, maybe a lot of a hack), and it will almost certainly break if the
        graph's data structure changes.

        If you want a deeper understanding of how this method works, let's look
        at an example of the graph data structure:

            graph_data: {
                "13": {
                    "inputs": {
                        "scheduler": "beta", "steps": 5, "denoise": 1.0,
                        "model": ["471", 0],
                    }, "class_type": "BasicScheduler", "_meta": {
                        "title": "BasicScheduler"
                    },
                }, "471": {
                    "inputs": {
                        "unet_name": "FLUX1\\flux1-schnell-Q4_K_S.gguf"
                    }, "class_type": "UnetLoaderGGUF", "_meta": {
                        "title": "Unet Loader (GGUF)"
                    },
                }, "617": {
                    "inputs": {
                        "widget_name": "steps", "any_input": ["13", 0]
                    }, "class_type": "JHGetWidgetValueIntNode", "_meta": {
                        "title": "Get Widget Value (Integer)"
                    }, "is_changed": [True],
                },
            }

        In this example, there are three nodes: 13, 471 and 617. Each node is
        associated with a dictionary containing its inputs, class type, and some
        metadata (which in this case is the node's user-friendly title). Given
        an upstream node ID (as an int) we can get that dictionary by using

            graph_data[str(node_id)]

        noting that the graph data structure keys are strings, not integers
        (it's a JSON thing). This returns us the upstream node's dictionary; the
        dictionary has a key called "inputs" which in turn is another dictionary
        that lists input names and their values. We get this dictionary by using

            graph_data[str(node_id)]["inputs"]

        and then we look for the value of the given widget name like so:

            graph_data[str(node_id)]["inputs"][widget_name]

        As you can see, if any part of this data structure changes, this method
        will break. The graph data structure has been stable for a while, so
        this should all be fine. 🤞

        Args:
            node_id (int): The ID of the upstream node. widget_name (str): The
            name of the widget to fetch the value for. graph_data (dict): The
            graph's prompt dictionary.

        Returns:
            The value of the widget.

        Raises:
            KeyError: If the node ID or widget name is not found in the graph.
        """
        _node: dict
        try:
            _node = graph_data[str(node_id)]
        except KeyError as exc:
            raise KeyError(
                f"Node {node_id} not found in graph data. Available nodes: "
                f"{list(graph_data.keys())}"
            ) from exc

        if "inputs" not in _node:
            raise KeyError(
                f"Node {node_id} does not contain 'inputs'. Node data: {_node}"
            )

        if widget_name not in _node["inputs"]:
            raise KeyError(
                f"Widget '{widget_name}' not found in inputs of node {node_id}. "
                f"Available widgets: {list(_node['inputs'].keys())}"
            )

        return _node["inputs"][widget_name]


class JHGetWidgetValueStringNode(JHGetWidgetValueNode):
    """
    A node that retrieves a widget's value as a string.

    Inherits from `JHGetWidgetValueNode` and converts the retrieved value to a
    string before returning it.

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

    Inherits from `JHGetWidgetValueNode` and converts the retrieved value to an
    integer before returning it. Raises a `ValueError` if the value cannot be
    converted to an integer.

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
            raise ValueError(
                f"""Widget "{widget_name}" has value "{widget_value}" which is not an integer"""
            ) from exc
        return (widget_value,)


class JHGetWidgetValueFloatNode(JHGetWidgetValueNode):
    """
    A node that retrieves a widget's value as a float.

    Inherits from `JHGetWidgetValueNode` and converts the retrieved value to a
    float before returning it. Raises a `ValueError` if the value cannot be
    converted to a float.

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
            raise ValueError(
                f"""Widget "{widget_name}" has value "{widget_value}" which is not a float"""
            ) from exc
        return (widget_value,)
