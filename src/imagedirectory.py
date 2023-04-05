from pathlib import Path
from typing import List, Tuple, Any

from image import Image, has_images


class ImageDirectory:
    __slots__ = "name", "path", "images"

    def __init__(self, name: str, path: Path, images: List[Image]):
        """
        Directory of images.

        Args:
            name: The directory's name
            path: filesystem path to the directory (typically a directory)
            images: list of Image objects
        """
        self.name = name
        self.path = path
        self.images = images

    def __repr__(self):
        return f"ImageDirectory({self.name!r}, {len(self.images)!r} images)"

    def __str__(self):
        return f"({self.name!s}, {len(self.images)!s} images)"

    @classmethod
    def from_dir_tuple(cls, dir_tuple: Tuple[Any, list, list]) -> "ImageDirectory":
        path = Path(dir_tuple[0])
        images = [Image.from_path_str(image, path) for image in dir_tuple[2]]
        return cls(path.name, path, images)


def is_image_directory(dir_tuple: Tuple[Any, list, list]) -> bool:
    """
    Returns true if the input dir has no subdirs and has at least one image file.

    Args:
        dir_tuple: tuple of dir info as output by os.walk.
    Returns: bool
    """
    path, sub_dirs, files = dir_tuple
    return not sub_dirs and has_images(files)
