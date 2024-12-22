from typing import Any

import pytest

from comfyui_jh_xmp_metadata_nodes.jh_get_widget_value_nodes import (
    JHGetWidgetValueFloatNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueNode,
    JHGetWidgetValueStringNode,
)


@pytest.fixture
def graph_data() -> dict[str, Any]:
    return {
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


@pytest.fixture
def graph_data_invalid() -> dict[str, Any]:
    return {
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


@pytest.fixture
def node() -> JHGetWidgetValueNode:
    return JHGetWidgetValueNode()


@pytest.fixture
def node_string() -> JHGetWidgetValueStringNode:
    return JHGetWidgetValueStringNode()


@pytest.fixture
def node_int() -> JHGetWidgetValueIntNode:
    return JHGetWidgetValueIntNode()


@pytest.fixture
def node_float() -> JHGetWidgetValueFloatNode:
    return JHGetWidgetValueFloatNode()


def test_input_types() -> None:
    input_types = JHGetWidgetValueNode.INPUT_TYPES()
    assert "required" in input_types and input_types["required"].keys() == {
        "any_input",
        "widget_name",
    }
    assert "optional" not in input_types
    assert "hidden" in input_types and input_types["hidden"].keys() == {"prompt"}


def test_is_changed() -> None:
    assert JHGetWidgetValueNode.IS_CHANGED() is True


def test_get_widget_value_valid(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    result = node.get_widget_value(("13", 0), "steps", graph_data)
    assert result == (5,)


def test_get_widget_value_invalid_node_id(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    with pytest.raises(KeyError):
        node.get_widget_value(("999", 0), "steps", graph_data)


def test_get_widget_value_invalid_widget_name(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    with pytest.raises(KeyError):
        node.get_widget_value(("13", 0), "invalid_widget", graph_data)


def test_get_widget_value_empty_widget_name(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    with pytest.raises(ValueError):
        node.get_widget_value(("13", 0), "", graph_data)


def test_get_widget_value_empty_graph_data(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any] = {}
) -> None:
    with pytest.raises(KeyError):
        node.get_widget_value(("13", 0), "steps", graph_data)


def test_get_widget_value_invalid_graph_data(
    node: JHGetWidgetValueNode, graph_data_invalid: dict[str, Any]
) -> None:
    with pytest.raises(KeyError):
        node.get_widget_value(("471", 0), "steps", graph_data_invalid)


def test_get_widget_value_invalid_node_id_type(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    with pytest.raises(ValueError):
        node.get_widget_value(("invalid_node_id", 0), "steps", graph_data)


def test_get_widget_value_string_node(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    result = node.get_widget_value(("13", 0), "scheduler", graph_data)
    assert result == ("beta",)


def test_get_widget_value_int_node(
    node: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    result = node.get_widget_value(("13", 0), "steps", graph_data)
    assert result == (5,)


def test_get_widget_value_int_node_invalid_value(
    node_int: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    with pytest.raises(ValueError):
        node_int.get_widget_value(("13", 0), "scheduler", graph_data)


def test_get_widget_value_float_node(
    node_float: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    result = node_float.get_widget_value(("13", 0), "denoise", graph_data)
    assert result == (1.0,)


def test_get_widget_value_float_node_invalid_value(
    node_float: JHGetWidgetValueNode, graph_data: dict[str, Any]
) -> None:
    with pytest.raises(ValueError):
        node_float.get_widget_value(("13", 0), "scheduler", graph_data)
