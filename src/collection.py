from pathlib import Path

from image import has_images, Image


class Collection(object):
    __slots__ = "name", "path", "images"

    def __init__(self, name: str, path: Path, images: list):
        self.name = name
        self.path = path
        self.images = images

    def __repr__(self):
        return f"Collection({self.name!r}, {len(self.images)!r} images)"

    def __str__(self):
        return f"({self.name!s}, {len(self.images)!s} images)"

    @classmethod
    def from_dir_tuple(cls, dir_tuple: tuple) -> 'Collection':
        path = Path(dir_tuple[0])
        images = [Image.from_path_str(image, path) for image in dir_tuple[2]]
        return cls(path.name, path, images)


def is_collection(dir_tuple: tuple) -> bool:
    """
    Returns true if the input dir has no subdirs and has at least
    one image file.
    :param dir_tuple: tuple of dir info as output by os.walk.
    :return: bool
    """
    path, sub_dirs, files = dir_tuple
    return not sub_dirs and has_images(files)
