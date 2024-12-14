import pytest
from src.jh_path_to_stem_node import JHPathToStemNode


def test_path_to_stem():
    path_to_stem = JHPathToStemNode()
    path = "/path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_empty_path():
    path_to_stem = JHPathToStemNode()
    path = ""
    expected_stem = ("",)
    assert path_to_stem.path_to_stem(path) == expected_stem


def test_path_to_stem_none_path():
    path_to_stem = JHPathToStemNode()
    path = None
    with pytest.raises(TypeError):
        path_to_stem.path_to_stem(path)


def test_INPUT_TYPES():
    input_types = JHPathToStemNode.INPUT_TYPES()
    expected_input_types = {
        "required": {
            "path": ("STRING",),
        },
    }
    assert input_types == expected_input_types


def test_RETURN_TYPES():
    return_types = JHPathToStemNode.RETURN_TYPES
    expected_return_types = ("STRING",)
    assert return_types == expected_return_types


def test_FUNCTION():
    function = JHPathToStemNode.FUNCTION
    expected_function = "path_to_stem"
    assert function == expected_function


def test_CATEGORY():
    category = JHPathToStemNode.CATEGORY
    expected_category = "XMP Metadata Nodes/Utilities"
    assert category == expected_category


def test_OUTPUT_NODE():
    output_node = JHPathToStemNode.OUTPUT_NODE
    expected_output_node = False
    assert output_node == expected_output_node


def test_path_to_stem_windows_path():
    path_to_stem = JHPathToStemNode()
    path = "C:\\path\\to\\file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_unix_path():
    path_to_stem = JHPathToStemNode()
    path = "/path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_relative_path():
    path_to_stem = JHPathToStemNode()
    path = "path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_absolute_path():
    path_to_stem = JHPathToStemNode()
    path = "/absolute/path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)
