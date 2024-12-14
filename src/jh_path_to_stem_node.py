"""
This module provides a utility node for extracting the stem (filename
without extension) from a given file path. It is intended for use within
the ComfyUI framework as part of the XMP Metadata Nodes package.
"""

from pathlib import Path


class JHPathToStemNode:
    """
    A utility node for extracting the stem (filename without extension)
    from a given file path.

    This node is designed for use within the ComfyUI framework. It
    defines a single required input for the file path and outputs the
    stem as a string.

    Input Types:
        - "path" (STRING): The file path to process.

    Return Types:
        - STRING: The extracted stem of the provided file path.

    Attributes:
        RETURN_TYPES (tuple): Specifies the return type of the node.
        FUNCTION (str): The function to be called when the node is executed.
        CATEGORY (str): The categorization of the node within the UI.
        OUTPUT_NODE (bool): Indicates if this node is an output node.

    Methods:
        - `path_to_stem`: Extracts the stem from the given file path.
    """

    @classmethod
    def INPUT_TYPES(cls):  # pylint: disable=invalid-name
        """
        Defines the input types for the `JHPathToStemNode`.

        Returns:
            dict: A dictionary with a single required input for the
            node, specifying the file path to process. The input is
            expected to be a string representing the path.
        """
        return {
            "required": {
                "path": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "path_to_stem"
    CATEGORY = "XMP Metadata Nodes/Utilities"
    OUTPUT_NODE = False

    def path_to_stem(self, path):
        """
        Extracts the stem (filename without extension) from the provided
        file path.

        Args:
            path (str): The file path to process.

        Returns:
            tuple: A tuple containing the stem (str) of the provided
            file path.

        Dependencies:
            - `pathlib.Path`: Used to extract the stem from the path.
        """
        return (Path(path).stem,)
