import pytest

from comfyui_jh_xmp_metadata_nodes.jh_format_metadata_node import JHFormatMetadataNode


@pytest.fixture
def node() -> JHFormatMetadataNode:
    return JHFormatMetadataNode()


def test_input_types(node: JHFormatMetadataNode) -> None:
    input_types = node.INPUT_TYPES()
    assert input_types.keys() == {"required", "optional"}
    assert "required" in input_types and input_types["required"].keys() == {
        "format_string"
    }
    assert "optional" in input_types and input_types["optional"].keys() == {
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


def test_format_metadata_default_format_string(node: JHFormatMetadataNode) -> None:
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


def test_format_metadata_custom_format_string(node: JHFormatMetadataNode) -> None:
    custom_format = "Custom Prompt: {prompt}"
    result = node.format_metadata(prompt="Test Prompt", format_string=custom_format)
    expected = "Custom Prompt: Test Prompt"
    assert result == (expected,)


def test_format_metadata_invalid_format_string(node: JHFormatMetadataNode) -> None:
    invalid_format = "Invalid {placeholder}"
    with pytest.raises(
        ValueError, match="Invalid placeholder 'placeholder' in format_string"
    ):
        node.format_metadata(format_string=invalid_format)


def test_format_metadata_all_fields_provided(node: JHFormatMetadataNode) -> None:
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


def test_format_metadata_partial_fields_provided(node: JHFormatMetadataNode) -> None:
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


def test_format_metadata_with_zero_values(node: JHFormatMetadataNode) -> None:
    result = node.format_metadata(
        prompt="Test Prompt",
        model_name="Test Model",
        seed=0,
        steps=0,
        cfg=0.0,
        guidance=0.0,
    )
    expected = (
        "Prompt: Test Prompt\n"
        "Negative Prompt: \n"
        "Model: Test Model\n"
        "Seed: 0\n"
        "Sampler: \n"
        "Scheduler: \n"
        "Steps: 0\n"
        "CFG: 0.0\n"
        "Guidance: 0.0"
    )
    assert result == (expected,)


def test_format_metadata_with_nested_placeholders(node: JHFormatMetadataNode) -> None:
    result = node.format_metadata(
        prompt="Test Prompt",
        format_string="Prompt: {{prompt}}",
    )
    expected = "Prompt: {prompt}"
    assert result == (expected,)


def test_format_metadata_with_unicode_format_string(node: JHFormatMetadataNode) -> None:
    result = node.format_metadata(
        prompt="Test Prompt",
        format_string="❤️: {prompt}",
    )
    expected = "❤️: Test Prompt"
    assert result == (expected,)


def test_format_metdata_with_empty_format_string(node: JHFormatMetadataNode) -> None:
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
        format_string="",
    )
    expected = ""
    assert result == (expected,)


def test_IS_CHANGED(node: JHFormatMetadataNode) -> None:
    # The IS_CHANGED method should always return True
    assert node.IS_CHANGED()
