import pytest

from ..comfyui_jh_xmp_metadata_nodes.jh_path_to_stem_node import JHPathToStemNode


@pytest.fixture
def node():
    return JHPathToStemNode()


def test_input_types(node: JHPathToStemNode):
    assert isinstance(node.INPUT_TYPES(), dict)
    assert "required" in node.INPUT_TYPES()
    assert "path" in node.INPUT_TYPES()["required"]


def test_path_to_stem_valid(node: JHPathToStemNode):
    result = node.path_to_stem("C:/Users/Example/file.txt")
    assert result == ("file",)


def test_path_to_stem_no_extension(node: JHPathToStemNode):
    result = node.path_to_stem("C:/Users/Example/file")
    assert result == ("file",)


def test_path_to_stem_hidden_file(node: JHPathToStemNode):
    result = node.path_to_stem("C:/Users/Example/.hiddenfile")
    assert result == (".hiddenfile",)


def test_path_to_stem_nested_path(node: JHPathToStemNode):
    result = node.path_to_stem("C:/Users/Example/folder/subfolder/file.txt")
    assert result == ("file",)


def test_path_to_stem_empty_string(node: JHPathToStemNode):
    result = node.path_to_stem("")
    assert result == ("",)
