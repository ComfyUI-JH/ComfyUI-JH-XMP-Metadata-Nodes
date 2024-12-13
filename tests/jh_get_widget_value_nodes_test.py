"""
Tests for JHGetWidgetValueNode and its derived classes.

This suite includes:
- Validation of widget value retrieval for String, Int, and Float nodes.
- Edge cases for empty prompts, invalid formats, whitespace handling, and type conversions.
- Tests for exception handling and performance under large prompts.
"""

import time

import pytest

from src.jh_get_widget_value_nodes import (
    JHGetWidgetValueFloatNode,
    JHGetWidgetValueIntNode,
    JHGetWidgetValueNode,
    JHGetWidgetValueStringNode,
)


@pytest.fixture
def prompt_fixture():
    """A sample prompt dictionary for testing."""
    return {
        "1": {"inputs": {"test_widget": "Hello, World!", "numeric_widget": "42"}},
        "2": {"inputs": {"float_widget": "3.14"}},
    }


@pytest.mark.parametrize(
    "node_class, any_input, widget_name, expected, exception, match",
    [
        # Base functionality
        (JHGetWidgetValueNode, ["1"], "test_widget", ("Hello, World!",), None, None),
        (JHGetWidgetValueNode, ["1"], "numeric_widget", ("42",), None, None),
        (
            JHGetWidgetValueNode,
            ["999"],
            "test_widget",
            None,
            KeyError,
            "Widget test_widget not found in node 999",
        ),
        (
            JHGetWidgetValueNode,
            ["1"],
            "non_existent_widget",
            None,
            KeyError,
            "Widget non_existent_widget not found in node 1",
        ),
        (
            JHGetWidgetValueNode,
            ["1"],
            "",
            None,
            ValueError,
            "widget_name must not be empty",
        ),
        # StringNode functionality
        (
            JHGetWidgetValueStringNode,
            ["1"],
            "test_widget",
            ("Hello, World!",),
            None,
            None,
        ),
        (JHGetWidgetValueStringNode, ["1"], "numeric_widget", ("42",), None, None),
        # IntNode functionality
        (JHGetWidgetValueIntNode, ["1"], "numeric_widget", (42,), None, None),
        (
            JHGetWidgetValueIntNode,
            ["1"],
            "test_widget",
            None,
            ValueError,
            'Widget "test_widget" is not an integer',
        ),
        # FloatNode functionality
        (JHGetWidgetValueFloatNode, ["2"], "float_widget", (3.14,), None, None),
        (
            JHGetWidgetValueFloatNode,
            ["1"],
            "test_widget",
            None,
            ValueError,
            'Widget "test_widget" is not a float',
        ),
    ],
)
def test_widget_value_retrieval(
    node_class, any_input, widget_name, expected, exception, match, prompt_fixture
):
    """Test widget value retrieval for multiple scenarios."""
    print(
        f"Testing {node_class.__name__} with any_input={any_input}, widget_name={widget_name}"
    )
    node = node_class()

    if exception:
        with pytest.raises(exception, match=match):
            node.get_widget_value(
                any_input=any_input, widget_name=widget_name, prompt=prompt_fixture
            )
    else:
        result = node.get_widget_value(
            any_input=any_input, widget_name=widget_name, prompt=prompt_fixture
        )
        assert result == expected, (
            f"{node_class.__name__}: For widget '{widget_name}' in nodes {any_input}, "
            f"expected {expected}, but got {result}."
        )


def test_empty_prompt():
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError, match="Widget test_widget not found"):
        node.get_widget_value(
            any_input=["1"],
            widget_name="test_widget",
            prompt={},
        ), "Expected KeyError for an empty prompt dictionary."


def test_invalid_float_format(prompt_fixture):
    node = JHGetWidgetValueFloatNode()
    with pytest.raises(ValueError, match='Widget "test_widget" is not a float'):
        node.get_widget_value(
            any_input=["1"],
            widget_name="test_widget",
            prompt={"1": {"inputs": {"test_widget": "3.14abc"}}},
        ), "Expected ValueError for a non-float value '3.14abc'."


def test_invalid_int_format(prompt_fixture):
    node = JHGetWidgetValueIntNode()
    with pytest.raises(ValueError, match='Widget "numeric_widget" is not an integer'):
        node.get_widget_value(
            any_input=["1"],
            widget_name="numeric_widget",
            prompt={"1": {"inputs": {"numeric_widget": "42.0"}}},
        ), "Expected ValueError for a non-integer value '42.0'."


def test_numeric_as_string(prompt_fixture):
    node = JHGetWidgetValueStringNode()
    result = node.get_widget_value(
        any_input=["1"], widget_name="numeric_widget", prompt=prompt_fixture
    )
    assert result == (
        "42",
    ), "Numeric data should be converted to string for StringNode."


def test_case_sensitivity(prompt_fixture):
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError, match="Widget Test_Widget not found in node 1"):
        node.get_widget_value(
            any_input=["1"], widget_name="Test_Widget", prompt=prompt_fixture
        )


def test_widget_name_with_whitespace(prompt_fixture):
    node = JHGetWidgetValueNode()
    with pytest.raises(KeyError, match="Widget  test_widget  not found in node 1"):
        node.get_widget_value(
            any_input=["1"], widget_name=" test_widget ", prompt=prompt_fixture
        )


def test_large_prompt_performance():
    large_prompt = {
        str(i): {"inputs": {"test_widget": f"Value {i}"}} for i in range(1000)
    }
    node = JHGetWidgetValueNode()

    start_time = time.time()
    result = node.get_widget_value(
        any_input=["999"], widget_name="test_widget", prompt=large_prompt
    )
    elapsed_time = time.time() - start_time

    assert result == ("Value 999",), "Performance issue with large prompts."
    assert elapsed_time < 1, (
        f"Performance issue: Retrieving 'test_widget' from a large prompt (1000 entries) "
        f"took {elapsed_time:.2f} seconds, exceeding the 1-second limit."
    )
