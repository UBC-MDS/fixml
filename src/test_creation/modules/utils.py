from typing import Union
from pathlib import Path


def get_extension(file_path: Union[str, Path]) -> str:
    """Process a string or a Path object, and returns the extension of the
    file.

    The extension returned does not start with a dot, and all characters are
    all converted to lower case.

    Parameters
    ----------
    file_path : Union[str, Path]
        The file path to input.

    Returns
    -------
    str
        The extracted and normalized extension of the file.
    """
    return Path(file_path).resolve().suffix.lstrip(".").lower()
