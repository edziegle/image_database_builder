from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Tuple

from pydantic import BaseModel

from .image import Image, has_images, is_image
from .mongo_support import PydanticObjectId as ObjectId


class ImageDirectory(BaseModel):
    name: str
    path: str
    image_ids: List[ObjectId] = []
    created_at: str = str(datetime.utcnow())
    updated_at: Optional[str] = None

    @classmethod
    def from_dir_tuple(
        cls, dir_tuple: Tuple[Any, list, list]
    ) -> Tuple["ImageDirectory", List[Image]]:
        """
        Creates an ImageDirectory object from a tuple of directory info as output by `os.walk`.
        Also creates a list of Image objects from the images in the directory.

        Args:
            dir_tuple: `os.walk` tuple of directory info.

        Returns: tuple of ImageDirectory and list of Image objects.

        """
        path = Path(dir_tuple[0])
        images = [
            Image.from_path_str(image, path.name)
            for image in dir_tuple[2]
            if is_image(image)
        ]
        return cls(name=path.name, path=path.as_uri()), images


def is_image_directory(dir_tuple: Tuple[Any, list, list]) -> bool:
    """
    Returns true if the input dir has no sub-dirs and has at least one image file.

    Args:
        dir_tuple: tuple of dir info as output by os.walk.
    Returns: bool
    """
    path, sub_dirs, files = dir_tuple
    return not sub_dirs and has_images(files)
