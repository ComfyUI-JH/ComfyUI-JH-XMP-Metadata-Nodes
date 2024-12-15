from src.any_type import AnyType

# pylint: disable=unnecessary-negation


def test_ne_method():
    any_type_instance = AnyType("test")
    assert not (any_type_instance != "test")
    assert not (any_type_instance != "different")
    assert not (any_type_instance != 123)
    assert not (any_type_instance != None)
