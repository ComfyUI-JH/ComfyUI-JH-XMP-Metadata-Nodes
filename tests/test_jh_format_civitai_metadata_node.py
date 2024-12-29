import pytest
from pytest_mock import MockerFixture

from comfyui_jh_xmp_metadata_nodes.jh_format_civitai_metadata_node import (
    JHFormatCivitaiMetadataNode,
)

# region Fixtures


@pytest.fixture
def node() -> JHFormatCivitaiMetadataNode:
    return JHFormatCivitaiMetadataNode()


# endregion Fixtures

# region Tests


def test_format_metadata(
    node: JHFormatCivitaiMetadataNode, mocker: MockerFixture
) -> None:
    mocker.patch(
        "comfyui_jh_xmp_metadata_nodes.jh_format_civitai_metadata_node.folder_paths.get_full_path",
        return_value="/mocked/path/model.safetensors",
    )

    formatted_metadata = node.format_metadata(
        prompt="Test Prompt",
        negative_prompt="Test Negative Prompt",
        seed=123,
        sampler_name="Test Sampler",
        scheduler_name="Test Scheduler",
        steps=10,
        cfg=1.0,
        guidance=1.0,
        model_path="model.safetensors",
        width=512,
        height=512,
    )

    assert "Test Prompt\n" in formatted_metadata[0]
    assert "Negative prompt: Test Negative Prompt\n" in formatted_metadata[0]
    assert "Steps: 10, " in formatted_metadata[0]
    assert "Sampler: Test Sampler_Test Scheduler, " in formatted_metadata[0]
    assert "CFG Scale: 1.0, " in formatted_metadata[0]
    assert "Guidance: 1.0, " in formatted_metadata[0]
    assert "Seed: 123, " in formatted_metadata[0]
    assert "Size: 512x512, " in formatted_metadata[0]
    assert "Model: model" in formatted_metadata[0]


# endregion Tests
