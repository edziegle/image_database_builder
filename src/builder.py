#!/usr/bin/env python3
import logging
from datetime import datetime
from errno import EEXIST
from os import walk
from pathlib import Path
from typing import Dict, List, Tuple, TypeAlias

from pymongo.collection import Collection
from tqdm import tqdm

from data_model.image import Image
from data_model.imagedirectory import ImageDirectory, is_image_directory
from data_model.mongo_support import PydanticObjectId as ObjectId
from data_model.subject import Subject, is_subject
from database import get_collection, get_db, get_db_client

ImageDirTuple: TypeAlias = Tuple[ImageDirectory, List[Image]]
SubjectTuple: TypeAlias = Tuple[Subject, List[ImageDirTuple]]


def scan(root_dir: str) -> Dict[str, List[SubjectTuple] | List[ImageDirTuple]]:
    """
    Finds all "collections" under a given directory.

    Note:
        A collection is defined as a flat folder (IE, no sub-folders) with image contents.
        Any non-image files will be ignored. So long as a folder contains one or more
        images and has no subdirectories, it will be treated as a collection.
    Args:
        root_dir: path to directory to recursively scan through.
    Returns: list of ImageDirectory objects.
    """
    scan_results = {"subjects": [], "image_directories": []}
    for dir_tuple in (
        x for x in walk(root_dir)
    ):  # exhausting the generator right away, may change later
        if is_image_directory(dir_tuple):
            scan_results["image_directories"].append(
                ImageDirectory.from_dir_tuple(dir_tuple)
            )
        elif is_subject(dir_tuple):
            logging.info(f"Found subject: {dir_tuple[0]}")
            subject = Subject(name=Path(dir_tuple[0]).name, path=dir_tuple[0])
            subjects_img_dirs = []
            for sub_dir in dir_tuple[1]:
                sub_dir_path = Path(dir_tuple[0]) / sub_dir
                sub_dir_tuple = next(
                    x for x in walk(sub_dir_path) if is_image_directory(x)
                )
                subjects_img_dirs.append(ImageDirectory.from_dir_tuple(sub_dir_tuple))

            scan_results["subjects"].append((subject, subjects_img_dirs))
        else:
            logging.info(f"Skipping: {dir_tuple[0]}")

    return scan_results


def make_sure_path_exists(path):
    try:
        Path(path).mkdir()
    except OSError as exception:
        if exception.errno != EEXIST:
            raise


def main(target_dir: Path):
    logging.info("Loading database.")
    db = get_db(get_db_client())
    image_dir_collection = get_collection(db, "image_directories")
    image_collection = get_collection(db, "images")

    logging.info(f'Collecting photos and sub-directories of "{target_dir}".')
    scan_results = scan(str(target_dir))

    subject_pbar = tqdm(
        scan_results["subjects"], desc="Inserting subjects into database", leave=False
    )
    for pair in subject_pbar:
        subject = pair[0]
        sub_dir_pairs = pair[1]
        for sub_dir_pair in sub_dir_pairs:
            image_dir_id = insert_image_dir(
                sub_dir_pair[0], sub_dir_pair[1], image_collection, image_dir_collection
            )
            subject.image_dir_ids.append(image_dir_id)

    # insert any image directories that are not part of a subject
    for sub_dir_pair in scan_results["image_directories"]:
        insert_image_dir(
            sub_dir_pair[0], sub_dir_pair[1], image_collection, image_dir_collection
        )

    logging.info("Complete.")


def insert_image_dir(
    image_dir: ImageDirectory,
    images: List[Image],
    image_collection: Collection,
    image_dir_collection: Collection,
) -> ObjectId:
    image_pbar = tqdm(images, desc="Images", unit="image", leave=False)
    for image in image_pbar:
        image_id = image_collection.insert_one(image.dict()).inserted_id
        image_dir.image_ids.append(image_id)
    return image_dir_collection.insert_one(image_dir.dict())


if __name__ == "__main__":
    log_dir = "logs"
    log_file = f"database-builder {datetime.now()}.log"
    make_sure_path_exists(log_dir)

    file_handler = logging.FileHandler(f"{log_dir}/{log_file}")
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[file_handler, stream_handler],
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    main(Path("/Users/ericziegler/dev/image_database_builder/bin/sampleindex"))
