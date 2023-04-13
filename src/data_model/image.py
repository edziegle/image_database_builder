import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from config import config

EXTENSIONS = config["images"]["extensions"].split(",")


class Image(BaseModel):
    path: str
    parent: str
    image_type: str
    metadata: dict
    created_at: str = str(datetime.utcnow())
    updated_at: Optional[str] = None

    @classmethod
    def from_path_str(cls, path: str, parent: str) -> "Image":
        image_type = mimetypes.guess_type(path)
        metadata = parse_metadata(path)
        return Image(
            path=path, parent=parent, image_type=image_type[0], metadata=metadata
        )

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
