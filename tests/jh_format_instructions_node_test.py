import pytest

from src.jh_format_instructions_node import JHFormatInstructionsNode


def test_default_format():
    node = JHFormatInstructionsNode()
    result = node.format_instructions(prompt="Generate an image")
    assert "Prompt: Generate an image" in result[0]
    assert "Steps:" in result[0]


def test_custom_format():
    node = JHFormatInstructionsNode()
    custom_format = "Model: {model_name}, Seed: {seed}"
    result = node.format_instructions(
        model_name="StableDiffusion", seed=1234, format_string=custom_format
    )
    assert result[0] == "Model: StableDiffusion, Seed: 1234"


def test_missing_placeholders():
    node = JHFormatInstructionsNode()
    custom_format = "Sampler: {sampler_name}, Unknown: {unknown}"
    with pytest.raises(ValueError):
        node.format_instructions(sampler_name="Euler", format_string=custom_format)


def test_partial_inputs():
    node = JHFormatInstructionsNode()
    result = node.format_instructions(prompt="Artistic render", steps=50)
    assert "Prompt: Artistic render" in result[0]
    assert "Steps: 50" in result[0]
    assert "Model:" in result[0]  # Placeholder with default empty value


def test_empty_format_string():
    node = JHFormatInstructionsNode()
    result = node.format_instructions(format_string="")
    assert result[0] == ""


def test_large_input():
    node = JHFormatInstructionsNode()
    long_prompt = "Generate " + "very " * 1000 + "detailed image"
    result = node.format_instructions(prompt=long_prompt)
    assert "very detailed image" in result[0]
    assert len(result[0]) > 5000


def test_validate_format_string_no_placeholders():
    node = JHFormatInstructionsNode()
    format_string = "This is a simple string without placeholders."
    result = node.format_instructions(format_string=format_string)
    assert result[0] == format_string


def test_multiple_missing_placeholders():
    node = JHFormatInstructionsNode()
    custom_format = "Prompt: {prompt}, Invalid: {invalid1}, More Invalid: {invalid2}"
    with pytest.raises(ValueError, match="Invalid placeholder 'invalid1'"):
        node.format_instructions(prompt="Test Prompt", format_string=custom_format)


def test_unicode_handling():
    node = JHFormatInstructionsNode()
    result = node.format_instructions(
        prompt="Generate 🌟 image", model_name="漢字Model"
    )
    assert "Generate 🌟 image" in result[0]
    assert "漢字Model" in result[0]


def test_empty_inputs_with_default_format():
    node = JHFormatInstructionsNode()
    result = node.format_instructions()
    assert "Prompt:" in result[0]
    assert "Steps:" in result[0]
    assert "Model:" in result[0]


def test_boundary_conditions():
    node = JHFormatInstructionsNode()
    result = node.format_instructions(steps=0, cfg=0.0, guidance=1e10)
    assert "Steps: 0" in result[0]
    assert "CFG: 0.0" in result[0]
    assert "Guidance: 10000000000.0" in result[0]


def test_stress_formatting():
    node = JHFormatInstructionsNode()
    result = node.format_instructions(
        prompt="Prompt " * 1000,
        model_name="Model " * 500,
        sampler_name="Sampler " * 500,
        scheduler_name="Scheduler " * 500,
        steps=123456,
        cfg=9.99,
        guidance=5.55,
    )
    assert len(result[0]) > 10000


def test_validate_format_string_error_message():
    node = JHFormatInstructionsNode()
    invalid_format = "This has {invalid} and {missing} placeholders."
    with pytest.raises(ValueError, match="Invalid placeholder 'invalid'"):
        node.format_instructions(format_string=invalid_format)


def test_out_of_order_placeholders():
    node = JHFormatInstructionsNode()
    custom_format = "Seed: {seed}, Model: {model_name}, Prompt: {prompt}"
    result = node.format_instructions(
        seed=42,
        model_name="TestModel",
        prompt="A test prompt",
        format_string=custom_format,
    )
    assert result[0] == "Seed: 42, Model: TestModel, Prompt: A test prompt"
