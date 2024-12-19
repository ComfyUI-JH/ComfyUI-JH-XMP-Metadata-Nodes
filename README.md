![ComfyUI_01011_](https://github.com/user-attachments/assets/d37df1a3-3baf-43f0-bd67-e75df631a265)

# JH XMP Metadata Nodes

![GitHub License](https://img.shields.io/github/license/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes/ci.yml)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes/main)

Custom nodes for ComfyUI for the loading and saving of metadata in (originally Adobe's, now ISO-standard) XMP format. For information about XMP, see https://www.adobe.com/products/xmp.html.

The following metadata properties are currently supported:

- dc:creator
- dc:title
- dc:description
- dc:subject
- photoshop:Instructions

In addition, the **Load Image With XMP Metadata** node and the **Save Image With XMP Metadata** both support raw XML output and input respectively.

# Getting Started

## Installing from GitHub

1. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

2. Clone this repository into the `custom_nodes` folder:

    ```
    cd ComfyUI/custom_nodes
    git clone https://github.com/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes.git
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

# Nodes

## Load Image With XMP Metadata

<img width="1261" alt="image" src="https://github.com/user-attachments/assets/4e0351ee-cdc8-48c2-a005-deeb5b88724b" />

Just like the built-in **Load Image** node except if XMP metadata is embedded in the image it will be parsed and made available on the node's outputs. The **xml_string** output carries the entire XML data structure including metadata which is not specifically supported by this package.

## Save Image With XMP Metadata

<img width="425" alt="image" src="https://github.com/user-attachments/assets/3e1ccdb0-1019-4dbd-a3fa-502b383c5b93" />

Saves any images piped into it with embedded XMP metadata. All inputs (except **images**) are optional. Can save in a variety of file formats: JPEG, PNG (with and without embedding the ComfyUI workflow), WebP (lossy and lossless).
