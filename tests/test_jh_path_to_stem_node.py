import pytest

from comfyui_jh_xmp_metadata_nodes.jh_path_to_stem_node import JHPathToStemNode


@pytest.fixture
def node() -> JHPathToStemNode:
    return JHPathToStemNode()


def test_input_types() -> None:
    input_types = JHPathToStemNode.INPUT_TYPES()
    assert input_types.keys() == {"required"}
    assert "required" in input_types and input_types["required"].keys() == {"path"}


def test_path_to_stem_valid_windows(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("C:/Users/Example/file.txt")
    assert result == ("file",)


def test_path_to_stem_valid_posix(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("/Users/Example/file.txt")
    assert result == ("file",)


def test_path_to_stem_no_extension_windows(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("C:/Users/Example/file")
    assert result == ("file",)


def test_path_to_stem_no_extension_posix(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("/Users/Example/file")
    assert result == ("file",)


def test_path_to_stem_hidden_file_windows(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("C:/Users/Example/.hiddenfile")
    assert result == (".hiddenfile",)


def test_path_to_stem_hidden_file_posix(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("/Users/Example/.hiddenfile")
    assert result == (".hiddenfile",)


def test_path_to_stem_nested_path_windows(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("C:/Users/Example/folder/subfolder/file.txt")
    assert result == ("file",)


def test_path_to_stem_nested_path_posix(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("/Users/Example/folder/subfolder/file.txt")
    assert result == ("file",)


def test_path_to_stem_empty_string(node: JHPathToStemNode) -> None:
    result = node.path_to_stem("")
    assert result == ("",)
