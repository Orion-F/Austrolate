"""
Module Name: file_util.py

Purpose: Define functions that help with using files.
"""

def get_file_as_string(file_path) -> str:
    """
    Returns: string of file contents.
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()