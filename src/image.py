import mimetypes
from pathlib import Path
from config import config

EXTENSIONS = config['images']['extensions'].split(",")


class Image(object):
    __slots__ = "path", "parent", "image_type", "metadata"

    def __init__(self, path: Path, parent: Path, image_type: str, metadata: dict):
        self.path = path
        self.parent = parent
        self.image_type = image_type
        self.metadata = metadata

    def __repr__(self):
        return f"Image({self.parent.name!r}: {self.path!r})"

    def __str__(self):
        return f"({self.parent.name!s}: {self.path!s})"

    @classmethod
    def from_path_str(cls, path: str, parent: Path) -> 'Image':
        image_type = mimetypes.guess_type(path)
        metadata = parse_metadata(path)
        return Image(Path(path), parent, image_type[0], metadata)

    def get_full_path(self) -> Path:
        return Path(self.parent, self.path)


def parse_metadata(path: str) -> dict:
    return {}


def is_image(image_name: str) -> bool:
    return any(image_name.endswith(ext) for ext in EXTENSIONS)


def has_images(files: list) -> bool:
    """
    Returns true if any file in the list is an image.
    :param files: list of files.
    :return: bool
    """
    return any((is_image(file) for file in files))


# todo might be able to combine get_images and has_images?
def get_images(files: list) -> list:
    return [file for file in files if is_image(file)]
