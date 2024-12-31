<div align="center">
    <img src="https://github.com/user-attachments/assets/d37df1a3-3baf-43f0-bd67-e75df631a265" />
</div>

<div align="center">
    <img src="https://img.shields.io/github/license/ComfyUI-JH/ComfyUI_JH_XMP_Metadata_Nodes">
    &emsp;
    <img src="https://img.shields.io/github/actions/workflow/status/ComfyUI-JH/ComfyUI-JH-XMP-Metadata-Nodes/ci.yml?label=ci">
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

Custom nodes for loading and saving images with embedded XMP metadata (https://www.adobe.com/products/xmp.html). Also included are nodes for saving images with [AUTOMATIC1111](https://github.com/AUTOMATIC1111) metadata for posting to [Civitai](https://civitai.com).

## About Metadata

When I generate tens or hundreds of images from ComfyUI they all go into a folder and get forgotten because I have no practical way to find them again. Embedded metadata solves this problem. When metadata is present in a file, both macOS and Windows index it automatically, making it searchable from the Finder on the Mac or the File Explorer in Windows.

<br />

<div align="center">
    <img width="250" alt="image" src="https://github.com/user-attachments/assets/7d7e5c93-fe33-409e-86fa-0a565bfdd6f1" align="middle" />
    &emsp;
    <img width="450" alt="image" src="https://github.com/user-attachments/assets/9effa555-1ddd-49c9-9459-53ceccdd9fef" align="middle"/>
</div>

<br />

<div align="center">
    <img width="250" alt="image" src="https://github.com/user-attachments/assets/46e429a8-4918-416a-98a7-cebf000b0756" align="middle" />
    &emsp;
    <img width="400" src="https://github.com/user-attachments/assets/664917ff-b87e-4a0c-8685-4e65c9299dad" align="middle" />
</div>

<br />

Apps like Photoshop and Lightroom expose XMP metadata and allow it to be viewed or edited.

<br />

<div align="center">
    <img width="400" alt="image" src="https://github.com/user-attachments/assets/3af31cad-9fca-4de4-97fe-f9c28cf65289" align="middle" />
    &emsp;
    <img width="244" alt="image" src="https://github.com/user-attachments/assets/cdb8f93a-8c30-4f32-9f2a-242bdcf42f62" align="middle" />
</div>

<br />

## Supported Properties

The following metadata properties are currently supported:

| Property | Description |
| --- | --- |
| dc:creator | A creator or list of creators of the image. Items can be separated by commas (`John Doe, Jane Doe`) or semicolons (`John Doe; Jane Doe`) |
| dc:rights | Information about the rights and clearances associated with the image, if any. |
| dc:title | A title for the image. |
| dc:description | A description of the image. |
| dc:subject | A subject or list of subjects. Items can be separated by commas (`wetsuit, sunset`) or semicolons (`wetsuit; sunset`) |
| photoshop:Instructions | Special instructions. |
| Iptc4xmpCore:AltTextAccessibility | Alt. text that can (in principle) be used by assistive technologies. |
| Iptc4xmpCore:ExtDescrAccessibility | A longer, more detailed elaboration of the Iptc4xmpCore:AltTextAccessibility property |

# Getting Started

## Installing with [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager) (Recommended)

<div align="center">
    <img width="1365" alt="image" src="https://github.com/user-attachments/assets/d703ca41-bd32-43bd-9360-ce0908880771" align="middle" />
</div>

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

<div align="center">
    <img width="1264" alt="image" src="https://github.com/user-attachments/assets/c511f418-fee2-48bb-9cb7-891312f46319" align="middle" />
</div>
<br />

Just like the built-in **Load Image** node except if XMP metadata is embedded in the image it will be parsed and made available on the node's outputs. The **xml_string** output carries the entire XML data structure including metadata which is not specifically supported by this package.

## Save Image With XMP Metadata

<div align="center">
    <img width="540" alt="image" src="https://github.com/user-attachments/assets/0b3c834d-8996-4a18-9ff2-0cc816115106" align="middle" />
</div>
<br />

Saves any images piped into it with embedded XMP metadata. All inputs (except **images**) are optional. Can save in a variety of file formats: JPEG, PNG (with and without embedding the ComfyUI workflow), WebP (lossy and lossless).

## Get Widget Value

<div align="center">
    <img width="1017" alt="image" src="https://github.com/user-attachments/assets/2369d34c-62c3-4bab-9b4b-9abf75aaa0b5" align="middle" />
</div>
<br />

Can be used to get the **string**, **int** or **float** value of any widget on any node. Simply pipe the node into this node's input and type in the name of the widget you want the value of.

## Path to Stem

<div align="center">
    <img width="1309" alt="image" src="https://github.com/user-attachments/assets/082f265d-898c-4437-a20f-9d3f5057a3cb" align="middle" />
</div>
<br />

Given a path string (absolute or relative), this node returns the "stem," meaning the filename alone minus any extension.

## Format Metadata

<div align="center">
    <img width="400" alt="image" src="https://github.com/user-attachments/assets/66065daf-3ba4-42b6-b0fa-72673d16aa25" align="middle" />
</div>
<br />

This utility node takes common workflow inputs (prompt, model_name, seed, etc.) and allows you to construct a string that can subsequently be piped into a **Save Image With XMP Metadata** node input to embed metadata however you choose.

## Format Civitai Metadata

<div align="center">
    <img width="473" alt="image" src="https://github.com/user-attachments/assets/b183d16e-89f7-4ad0-a9d6-81626c5d66e2" align="middle" />
</div>
<br />

This utility node takes common workflow inputs (prompt, model_name, seed, etc.) and outputs metadata in the [AUTOMATIC1111](https://github.com/AUTOMATIC1111) format which can be read by [Civitai](https://civitai.com). Pipe this node's output into the **civitai_metadata** input on the **Save Image With XMP Metadata** node to embed this metadata in your saved images.

# Credits

This software includes source code from other products:

| Product | Code Used | License |
| --- | --- | --- |
| [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | Code from the **Load Image** and **Save Image** nodes. | ![GitHub License](https://img.shields.io/github/license/comfyanonymous/ComfyUI) |
| [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts) | The **AnyType** class and its implementation. | ![GitHub License](https://img.shields.io/github/license/pythongosssss/ComfyUI-Custom-Scripts) |
