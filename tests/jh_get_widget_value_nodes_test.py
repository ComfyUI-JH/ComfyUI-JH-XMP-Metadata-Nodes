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
        assert result == expected, f"Expected {expected}, got {result}."
