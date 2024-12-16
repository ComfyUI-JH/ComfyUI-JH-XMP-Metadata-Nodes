from typing import Any

import pytest

from src.any_type import AnyType
from src.jh_get_widget_value_nodes import (
    JHGetWidgetValueFloatNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueNode,
    JHGetWidgetValueStringNode,
)

# pylint: disable=redefined-outer-name


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


def test_input_types() -> None:
    expected_input_types = {
        "required": {
            "any_input": (AnyType("*"), {"rawLink": True}),
            "widget_name": ("STRING", {"multiline": False}),
        },
        "hidden": {
            "prompt": "PROMPT",
        },
    }
    assert JHGetWidgetValueNode.INPUT_TYPES() == expected_input_types


def test_is_changed() -> None:
    assert JHGetWidgetValueNode.IS_CHANGED() is True


def test_get_widget_value_valid(graph_data: dict[str, Any]) -> None:
    node = JHGetWidgetValueNode()
    result = node.get_widget_value(("13", 0), "steps", graph_data)
    assert result == (5,)


def test_get_widget_value_invalid_node_id(graph_data: dict[str, Any]):
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError):
        node.get_widget_value(("999", 0), "steps", graph_data)


def test_get_widget_value_invalid_widget_name(graph_data: dict[str, Any]):
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError):
        node.get_widget_value(("13", 0), "invalid_widget", graph_data)


def test_get_widget_value_empty_widget_name(graph_data: dict[str, Any]):
    node = JHGetWidgetValueNode()
    with pytest.raises(ValueError):
        node.get_widget_value(("13", 0), "", graph_data)


def test_get_widget_value_empty_graph_data():
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError):
        node.get_widget_value(("13", 0), "steps", {})


def test_get_widget_value_invalid_graph_data(graph_data_invalid: dict[str, Any]):
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError):
        node.get_widget_value(("471", 0), "steps", graph_data_invalid)


def test_get_widget_value_invalid_node_id_type(graph_data: dict[str, Any]):
    node = JHGetWidgetValueNode()
    with pytest.raises(ValueError):
        node.get_widget_value(("invalid_node_id", 0), "steps", graph_data)


def test_get_widget_value_string_node(graph_data: dict[str, Any]):
    node = JHGetWidgetValueStringNode()
    result = node.get_widget_value(("13", 0), "scheduler", graph_data)
    assert result == ("beta",)


def test_get_widget_value_int_node(graph_data: dict[str, Any]):
    node = JHGetWidgetValueIntNode()
    result = node.get_widget_value(("13", 0), "steps", graph_data)
    assert result == (5,)


def test_get_widget_value_int_node_invalid_value(graph_data: dict[str, Any]):
    node = JHGetWidgetValueIntNode()
    with pytest.raises(ValueError):
        node.get_widget_value(("13", 0), "scheduler", graph_data)


def test_get_widget_value_float_node(graph_data: dict[str, Any]):
    node = JHGetWidgetValueFloatNode()
    result = node.get_widget_value(("13", 0), "denoise", graph_data)
    assert result == (1.0,)


def test_get_widget_value_float_node_invalid_value(graph_data: dict[str, Any]):
    node = JHGetWidgetValueFloatNode()
    with pytest.raises(ValueError):
        node.get_widget_value(("13", 0), "scheduler", graph_data)
