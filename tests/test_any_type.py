from ..comfyui_jh_xmp_metadata_nodes.any_type import AnyType


def test_ne_method():
    any_type_instance = AnyType("test")
    assert not (any_type_instance != "test")
    assert not (any_type_instance != "different")
