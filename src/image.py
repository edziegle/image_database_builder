from pathlib import Path

EXTENSIONS = ('.jpeg', '.jpg', '.png', '.gif')


class Image(object):
    __slots__ = "path", "image_type", "metadata"

    def __init__(self, path: Path, image_type: str, metadata: dict):
        self.path = path
        self.image_type = image_type
        self.metadata = metadata


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
