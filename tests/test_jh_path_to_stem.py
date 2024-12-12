import pytest
from src.jh_path_to_stem import JHPathToStem


def test_path_to_stem():
    path_to_stem = JHPathToStem()
    path = "/path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_empty_path():
    path_to_stem = JHPathToStem()
    path = ""
    expected_stem = ("",)
    assert path_to_stem.path_to_stem(path) == expected_stem


def test_path_to_stem_none_path():
    path_to_stem = JHPathToStem()
    path = None
    with pytest.raises(TypeError):
        path_to_stem.path_to_stem(path)


def test_INPUT_TYPES():
    input_types = JHPathToStem.INPUT_TYPES()
    expected_input_types = {
        "required": {
            "path": ("STRING",),
        },
    }
    assert input_types == expected_input_types


def test_RETURN_TYPES():
    return_types = JHPathToStem.RETURN_TYPES
    expected_return_types = ("STRING",)
    assert return_types == expected_return_types


def test_FUNCTION():
    function = JHPathToStem.FUNCTION
    expected_function = "path_to_stem"
    assert function == expected_function


def test_CATEGORY():
    category = JHPathToStem.CATEGORY
    expected_category = "XMP Metadata Nodes/Utilities"
    assert category == expected_category


def test_OUTPUT_NODE():
    output_node = JHPathToStem.OUTPUT_NODE
    expected_output_node = False
    assert output_node == expected_output_node


def test_path_to_stem_windows_path():
    path_to_stem = JHPathToStem()
    path = "C:\\path\\to\\file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_unix_path():
    path_to_stem = JHPathToStem()
    path = "/path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_relative_path():
    path_to_stem = JHPathToStem()
    path = "path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)


def test_path_to_stem_absolute_path():
    path_to_stem = JHPathToStem()
    path = "/absolute/path/to/file.txt"
    expected_stem = "file"
    assert path_to_stem.path_to_stem(path) == (expected_stem,)
