import pytest

from comfyui_jh_xmp_metadata_nodes.jh_format_metadata_node import JHFormatMetadataNode


@pytest.fixture
def node() -> JHFormatMetadataNode:
    return JHFormatMetadataNode()


def test_input_types(node: JHFormatMetadataNode) -> None:
    input_types = node.INPUT_TYPES()
    assert input_types.keys() == {"required", "optional"}
    assert input_types["required"].keys() == {"format_string"}
    assert input_types["optional"].keys() == {
        "prompt",
        "negative_prompt",
        "model_name",
        "seed",
        "sampler_name",
        "scheduler_name",
        "steps",
        "cfg",
        "guidance",
    }


def test_IS_CHANGED(node: JHFormatMetadataNode) -> None:
    # The IS_CHANGED method should always return True
    assert node.IS_CHANGED()


def test_default_format_string(node: JHFormatMetadataNode) -> None:
    result = node.format_metadata()
    expected = (
        "Prompt: \n"
        "Negative Prompt: \n"
        "Model: \n"
        "Seed: \n"
        "Sampler: \n"
        "Scheduler: \n"
        "Steps: \n"
        "CFG: \n"
        "Guidance: "
    )
    assert result == (expected,)


def test_custom_format_string(node: JHFormatMetadataNode) -> None:
    custom_format = "Custom Prompt: {prompt}"
    result = node.format_metadata(prompt="Test Prompt", format_string=custom_format)
    expected = "Custom Prompt: Test Prompt"
    assert result == (expected,)


def test_missing_placeholder_in_format_string(node: JHFormatMetadataNode):
    invalid_format = "Invalid {missing_placeholder}"
    with pytest.raises(
        ValueError, match="Invalid placeholder 'missing_placeholder' in format_string"
    ):
        node.format_metadata(format_string=invalid_format)


def test_all_fields_provided(node: JHFormatMetadataNode) -> None:
    result = node.format_metadata(
        prompt="Test Prompt",
        negative_prompt="Test Negative",
        model_name="Test Model",
        seed=123,
        sampler_name="Test Sampler",
        scheduler_name="Test Scheduler",
        steps=50,
        cfg=7.5,
        guidance=1.0,
    )
    expected = (
        "Prompt: Test Prompt\n"
        "Negative Prompt: Test Negative\n"
        "Model: Test Model\n"
        "Seed: 123\n"
        "Sampler: Test Sampler\n"
        "Scheduler: Test Scheduler\n"
        "Steps: 50\n"
        "CFG: 7.5\n"
        "Guidance: 1.0"
    )
    assert result == (expected,)


def test_partial_fields_provided(node: JHFormatMetadataNode) -> None:
    result = node.format_metadata(
        prompt="Test Prompt",
        model_name="Test Model",
        steps=50,
    )
    expected = (
        "Prompt: Test Prompt\n"
        "Negative Prompt: \n"
        "Model: Test Model\n"
        "Seed: \n"
        "Sampler: \n"
        "Scheduler: \n"
        "Steps: 50\n"
        "CFG: \n"
        "Guidance: "
    )
    assert result == (expected,)
