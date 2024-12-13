import pytest
from src.any_type import AnyType
from src.jh_get_widget_value_nodes import (
    JHGetWidgetValueNode,
    JHGetWidgetValueStringNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueFloatNode,
)

any_type = AnyType("*")


def test_JHGetWidgetValueNode_IS_CHANGED():
    assert JHGetWidgetValueNode.IS_CHANGED() is True


def test_JHGetWidgetValueNode_INPUT_TYPES():
    input_types = JHGetWidgetValueNode.INPUT_TYPES()
    expected_input_types = {
        "required": {
            "any_input": (any_type, {"rawLink": True}),
            "widget_name": ("STRING", {"multiline": False}),
        },
        "hidden": {
            "prompt": "PROMPT",
        },
    }
    assert input_types == expected_input_types


def test_JHGetWidgetValueNode_get_widget_value_valid_input():
    node = JHGetWidgetValueNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": "widget_value"}}}
    result = node.get_widget_value(any_input, widget_name, prompt)
    assert result == ("widget_value",)


def test_JHGetWidgetValueNode_get_widget_value_empty_widget_name():
    node = JHGetWidgetValueNode()
    any_input = ["node_id"]
    widget_name = ""
    prompt = {"node_id": {"inputs": {"widget_name": "widget_value"}}}
    with pytest.raises(ValueError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueNode_get_widget_value_widget_not_found():
    node = JHGetWidgetValueNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {}}}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueNode_get_widget_value_invalid_prompt():
    node = JHGetWidgetValueNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueStringNode_get_widget_value_valid_input():
    node = JHGetWidgetValueStringNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": "widget_value"}}}
    result = node.get_widget_value(any_input, widget_name, prompt)
    assert result == ("widget_value",)


def test_JHGetWidgetValueStringNode_get_widget_value_empty_widget_name():
    node = JHGetWidgetValueStringNode()
    any_input = [0]
    widget_name = ""
    prompt = {"0": {"inputs": {"widget_name": "widget_value"}}}
    with pytest.raises(ValueError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueStringNode_get_widget_value_widget_not_found():
    node = JHGetWidgetValueStringNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {}}}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueStringNode_get_widget_value_invalid_prompt():
    node = JHGetWidgetValueStringNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueStringNode_get_widget_value_non_string_value():
    node = JHGetWidgetValueStringNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": 123}}}
    result = node.get_widget_value(any_input, widget_name, prompt)
    assert result == ("123",)


def test_JHGetWidgetValueIntNode_get_widget_value_valid_input():
    node = JHGetWidgetValueIntNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": 123}}}
    result = node.get_widget_value(any_input, widget_name, prompt)
    assert result == (123,)


def test_JHGetWidgetValueIntNode_get_widget_value_invalid_input():
    node = JHGetWidgetValueIntNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": "not an integer"}}}
    with pytest.raises(ValueError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueIntNode_get_widget_value_widget_not_found():
    node = JHGetWidgetValueIntNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {}}}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueIntNode_get_widget_value_empty_widget_name():
    node = JHGetWidgetValueIntNode()
    any_input = [0]
    widget_name = ""
    prompt = {"0": {"inputs": {"widget_name": 123}}}
    with pytest.raises(ValueError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueIntNode_get_widget_value_invalid_prompt():
    node = JHGetWidgetValueIntNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueFloatNode_get_widget_value_valid_input():
    node = JHGetWidgetValueFloatNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": 123.45}}}
    result = node.get_widget_value(any_input, widget_name, prompt)
    assert result == (123.45,)


def test_JHGetWidgetValueFloatNode_get_widget_value_invalid_input():
    node = JHGetWidgetValueFloatNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": "not a float"}}}
    with pytest.raises(ValueError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueFloatNode_get_widget_value_widget_not_found():
    node = JHGetWidgetValueFloatNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {}}}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueFloatNode_get_widget_value_empty_widget_name():
    node = JHGetWidgetValueFloatNode()
    any_input = [0]
    widget_name = ""
    prompt = {"0": {"inputs": {"widget_name": 123.45}}}
    with pytest.raises(ValueError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueFloatNode_get_widget_value_invalid_prompt():
    node = JHGetWidgetValueFloatNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {}
    with pytest.raises(KeyError):
        node.get_widget_value(any_input, widget_name, prompt)


def test_JHGetWidgetValueFloatNode_get_widget_value_integer_input():
    node = JHGetWidgetValueFloatNode()
    any_input = [0]
    widget_name = "widget_name"
    prompt = {"0": {"inputs": {"widget_name": 123}}}
    result = node.get_widget_value(any_input, widget_name, prompt)
    assert result == (123.0,)
