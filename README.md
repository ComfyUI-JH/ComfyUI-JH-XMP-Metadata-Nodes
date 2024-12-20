<div align="center">
    <img src="https://github.com/user-attachments/assets/d37df1a3-3baf-43f0-bd67-e75df631a265" />
</div>

<div align="center">
    <img src="https://img.shields.io/github/license/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes">
    &emsp;
    <img src="https://img.shields.io/github/actions/workflow/status/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes/ci.yml">
    &emsp;
    <img src="https://img.shields.io/github/last-commit/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes/main">
    &emsp;
    <img src="https://img.shields.io/github/issues/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes">
    &emsp;
    <img src="https://img.shields.io/github/issues-pr/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes">
</div>

<div align="center">

---
[**Getting Started**](#getting-started) | [**Nodes**](#nodes) | [**Credits**](#credits)
---

</div>


# JH XMP Metadata Nodes

These are custom nodes for ComfyUI for the loading and saving of metadata in XMP format. XMP metadata is embedded in the images created by these nodes; it travels along wherever the image does. Both macOS and Windows index XMP metadata automatically, making it searchable from the Finder on the Mac or the File Explorer in Windows. Apps like Photoshop or Lightroom (and presumably many others) expose XMP metadata and allow it to be edited.

<details>
    <summary>macOS</summary>
    <br />
    <div align="center">
        <img width="250" alt="image" src="https://github.com/user-attachments/assets/7d7e5c93-fe33-409e-86fa-0a565bfdd6f1" align="middle" />
        &emsp;
        <img width="450" alt="image" src="https://github.com/user-attachments/assets/9effa555-1ddd-49c9-9459-53ceccdd9fef" align="middle"/>
    </div>
    <br />
</details>

<details>
    <summary>Windows</summary>
    <br />
    <div align="center">
        <img width="250" alt="image" src="https://github.com/user-attachments/assets/46e429a8-4918-416a-98a7-cebf000b0756" align="middle" />
        &emsp;
        <img width="400" src="https://github.com/user-attachments/assets/664917ff-b87e-4a0c-8685-4e65c9299dad" align="middle" />
    </div>
    <br />
</details>

<details>
    <summary>Photoshop</summary>
    <br />
    <div align="center">
        <img width="400" alt="image" src="https://github.com/user-attachments/assets/3af31cad-9fca-4de4-97fe-f9c28cf65289" align="middle" />
    </div>
    <br />
</details>


## Supported Properties

The following metadata properties are currently supported:

| Property | Description |
| --- | --- |
| dc:creator | A creator of list of creators of the image. Items can be separated by commas (`John Doe, Jane Doe`) or semicolons (`John Doe; Jane Doe`) |
| dc:title | A title for the image. |
| dc:description | A description of the image. |
| dc:subject | A subject or list of subjects. Items can be separated by commas (`wetsuit, sunset`) or semicolons (`wetsuit; sunset`) |
| photoshop:Instructions | Special instructions. |
| exif:UserComment | Any user-provided comment about the image. |
| Iptc4xmpCore:AltTextAccessibility | Alt. text that can (in principle) be used by assistive technologies. |
| Iptc4xmpCore:ExtDescrAccessibility | A longer, more detailed elaboration of the Iptc4xmpCore:AltTextAccessibility property |

For more information about XMP, see https://www.adobe.com/products/xmp.html.

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

<details>
    <summary>Load Image With XMP Metadata</summary>
    <div align="center">
        <br />
        <img width="1128" alt="image" src="https://github.com/user-attachments/assets/8ce6fbf8-7d35-4041-9e22-2841fb1d1239" align="middle" />
    </div>
    <br />

Just like the built-in **Load Image** node except if XMP metadata is embedded in the image it will be parsed and made available on the node's outputs. The **xml_string** output carries the entire XML data structure including metadata which is not specifically supported by this package.

</details>

<details>
    <summary>Save Image With XMP Metadata</summary>
    <div align="center">
        <br />
        <img width="559" alt="image" src="https://github.com/user-attachments/assets/09934810-bdda-4333-9fcd-340f415222c3" align="middle" />
    </div>
    <br />

Saves any images piped into it with embedded XMP metadata. All inputs (except **images**) are optional. Can save in a variety of file formats: JPEG, PNG (with and without embedding the ComfyUI workflow), WebP (lossy and lossless).

</details>

<details>
    <summary>Get Widget Value</summary>
    <div align="center">
        <br />
        <img width="1035" alt="image" src="https://github.com/user-attachments/assets/f77b5747-3270-4007-b569-f77c81e01311" align="middle" />
    </div>
    <br />

Can be used to get the **string**, **int** or **float** value of any widget on any node. Simply pipe the node into this node's input and type in the name of the widget you want the value of.

</details>

<details>
    <summary>Path to Stem</summary>
    <div align="center">
        <br />
        <img width="1281" alt="image" src="https://github.com/user-attachments/assets/9541de76-2b1b-41af-820c-ab535404fd63" align="middle" />
    </div>
    <br />

Given a path string (absolute or relative), this node returns the "stem," meaning the filename alone minus any extension.

</details>

<details>
    <summary>Format Metadata</summary>
    <div align="center">
        <br />
        <img width="633" alt="image" src="https://github.com/user-attachments/assets/5be86083-6c3d-48f6-a0b5-60d45202af3c" />
    </div>
    <br />

This utility node takes common workflow inputs (prompt, model_name, seed, etc.) and allows you to construct a string that can subsequently be piped into a **Save Image With XMP Metadata** node input to embed metadata however you choose.

</details>

# Credits

This software includes source code from other products:

| Product | Code Used | License |
| --- | --- | --- |
| [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | Code from the **Load Image** and **Save Image** nodes. | ![GitHub License](https://img.shields.io/github/license/comfyanonymous/ComfyUI) |
| [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts) | The **AnyType** class and its implementation. | ![GitHub License](https://img.shields.io/github/license/pythongosssss/ComfyUI-Custom-Scripts) |
