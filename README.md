![ComfyUI_01011_](https://github.com/user-attachments/assets/d37df1a3-3baf-43f0-bd67-e75df631a265)

# JH XMP Metadata Nodes

![GitHub License](https://img.shields.io/github/license/jefferyharrell/ComfyUI_JH_XMP_Metadata_Nodes)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jefferyharrell/ComfyUI_JH_XMP_Metadata_Nodes/ci.yml)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/jefferyharrell/ComfyUI_JH_XMP_Metadata_Nodes/main)

Custom nodes for ComfyUI for the loading and saving of metadata in (originally Adobe's, now ISO-standard) XMP format. For information about XMP, see https://www.adobe.com/products/xmp.html.

# Getting Started

## Installing from GitHub

1. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

2. Clone this repository into the `custom_nodes` folder:

    ```
    cd ComfyUI/custom_nodes
    git clone https://github.com/jefferyharrell/ComfyUI_JH_XMP_Metadata_Nodes.git
    ```

3. Install the required Python packages. If you're using `venv` and `pip` that looks like this:

    ```
    cd ComfyUI_JH_Misc_Nodes
    pip install -r requirements.txt
    ```

    If you're using [Poetry](https://python-poetry.org/), then it's just

    ```
    cd ComfyUI_JH_Misc_Nodes
    poetry install
    ```
