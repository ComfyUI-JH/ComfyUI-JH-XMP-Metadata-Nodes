from typing import Any, Literal

from comfyui_jh_xmp_metadata_nodes import jh_types


class JHGetWidgetValueNode:
    @classmethod
    def IS_CHANGED(
        cls,
        *args: tuple[Any],
        **kwargs: dict[str, Any],
    ) -> Literal[True]:
        return True

    @classmethod
    def VALIDATE_INPUTS(
        cls, any_input: list[str | int], widget_name: str
    ) -> Literal[True]:
        return True

    @classmethod
    def INPUT_TYPES(cls) -> jh_types.JHInputTypesType:
        # fmt: off
        return {
            "required": {
                "any_input": (
                    jh_types.JHAnyType("*"),
                    {
                        "rawLink": True
                    }
                ),
                "widget_name": (
                    jh_types.JHNodeInputOutputTypeEnum.STRING,
                    {
                        "multiline": False
                    },
                ),
            },
            "hidden": {
                "prompt": jh_types.JHNodeInputOutputTypeEnum.PROMPT,
            },
        }
        # fmt: on

    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.PRIMITIVE,)
    OUTPUT_NODE = False
    FUNCTION = "get_widget_value"
    CATEGORY = "XMP Metadata Nodes/Utilities"

    def get_widget_value(
        self, any_input: tuple[str, int], widget_name: str, prompt: dict[str, Any]
    ) -> tuple[Any]:
        if widget_name == "":
            raise ValueError("widget_name must not be empty")

        upstream_node_id = int(any_input[0])
        widget_value: str = self._get_widget_value_from_graph(
            upstream_node_id, widget_name, prompt
        )
        return (widget_value,)

    @staticmethod
    def _get_widget_value_from_graph(
        node_id: int, widget_name: str, graph_data: dict[str, Any]
    ) -> str:
        """
        Retrieves the value of a widget from the graph's internal data
        structure.

        This method handles the tricky business of digging into the
        graph's internals, so if ComfyUI changes how the graph is
        structured in the future, you'll only need to fix it here. Right
        now, it's a bit of a hack (okay, maybe a lot of a hack), and it
        will almost certainly break if the graph's data structure
        changes.

        If you want a deeper understanding of how this method works,
        let's look at an example of the graph data structure:

            ```python
            graph_data: {
                "13": {
                    "inputs": {
                        "scheduler": "beta",
                        "steps": 5,
                        "denoise": 1.0,
                        "model": ["471", 0],
                    },
                    "class_type": "BasicScheduler",
                    "_meta": {"title": "BasicScheduler"},
                },
                "471": {
                    "inputs": {"unet_name": "FLUX1\\flux1-schnell-Q4_K_S.gguf"},
                    "class_type": "UnetLoaderGGUF",
                    "_meta": {"title": "Unet Loader (GGUF)"},
                },
                "617": {
                    "inputs": {"widget_name": "steps", "any_input": ["13", 0]},
                    "class_type": "JHGetWidgetValueIntNode",
                    "_meta": {"title": "Get Widget Value (Integer)"},
                    "is_changed": [True],
                },
            }
            ```

        In this example, there are three nodes: 13, 471 and 617. Each
        node is associated with a dictionary containing its inputs,
        class type, and some metadata (which in this case is the node's
        user-friendly title). Given an upstream node ID (as an int) we
        can get that dictionary by using

            ```python
            graph_data[str(node_id)]
            ```

        noting that the graph data structure keys are strings, not
        integers (it's a JSON thing). This returns us the upstream
        node's dictionary; the dictionary has a key called "inputs"
        which in turn is another dictionary that lists input names and
        their values. We get this dictionary by using

            ```python
            graph_data[str(node_id)]["inputs"]
            ```

        and then we look for the value of the given widget name like so:

            ```python
            graph_data[str(node_id)]["inputs"][widget_name]
            ```

        As you can see, if any part of this data structure changes, this
        method will break. The graph data structure has been stable for
        a while, so this should all be fine. 🤞

        Args:
            node_id (int): The ID of the upstream node.
            widget_name (str): The name of the widget to fetch the value for.
            graph_data (dict): The graph's prompt dictionary.

        Returns:
            The value of the widget.

        Raises:
            KeyError: If the node ID or widget name is not found in the graph.
        """
        _node: dict[str, Any]
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
    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.STRING,)

    def get_widget_value(
        self,
        any_input: tuple[str, int],
        widget_name: str,
        prompt: dict[str, Any],
    ) -> tuple[str]:
        widget_value = str(super().get_widget_value(any_input, widget_name, prompt)[0])
        return (widget_value,)


class JHGetWidgetValueIntNode(JHGetWidgetValueNode):
    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.INT,)

    def get_widget_value(
        self,
        any_input: tuple[str, int],
        widget_name: str,
        prompt: dict[str, Any],
    ) -> tuple[int]:
        widget_value = None
        try:
            widget_value = int(
                super().get_widget_value(any_input, widget_name, prompt)[0]
            )
        except ValueError as exc:
            raise ValueError(
                f"""Widget "{widget_name}" has value "{widget_value}" which is not an integer"""  # noqa: E501
            ) from exc
        return (widget_value,)


class JHGetWidgetValueFloatNode(JHGetWidgetValueNode):
    RETURN_TYPES = (jh_types.JHNodeInputOutputTypeEnum.FLOAT,)

    def get_widget_value(
        self,
        any_input: tuple[str, int],
        widget_name: str,
        prompt: dict[str, Any],
    ) -> tuple[float]:
        widget_value = None
        try:
            widget_value = float(
                super().get_widget_value(any_input, widget_name, prompt)[0]
            )
        except ValueError as exc:
            raise ValueError(
                f"""Widget "{widget_name}" has value "{widget_value}" which is not a float"""  # noqa: E501
            ) from exc
        return (widget_value,)
