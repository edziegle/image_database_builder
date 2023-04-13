from pathlib import Path
from typing import Any, List, Tuple

from pydantic import BaseModel

from .imagedirectory import is_image_directory
from .mongo_support import PydanticObjectId as ObjectId


class Subject(BaseModel):
    """
    A 'subject' is a collection of image directories. For example, a subject could be a person, a place, or a thing.
    """

    name: str
    path: str
    image_dir_ids: List[ObjectId] = []


def is_subject(dir_tuple: Tuple[Any, list, list]) -> bool:
    """
    Returns true if the input dir has at least one image sub-dir.

    Args:
        dir_tuple: `os.walk` tuple of directory info.

    Returns: true

    """
    path_raw, sub_dirs, files = dir_tuple
    path = Path(path_raw)
    for sub_dir in sub_dirs:
        path_to_sub_dir = Path(path, sub_dir)
        files_in_subdir = [
            str(file) for file in path_to_sub_dir.iterdir() if file.is_file()
        ]
        if is_image_directory((str(path_to_sub_dir), [], files_in_subdir)):
            return True
    return False
