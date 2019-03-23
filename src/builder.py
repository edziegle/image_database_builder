#!/usr/bin/env python3
import logging
from errno import EEXIST
from os import walk
from pathlib import Path
from datetime import datetime

import click

from collection import Collection, is_collection
from database import initialize_database, get_session, CollectionRecord, ImageRecord, Session


def scan(root_dir: str) -> list:
    """
    Finds all "collections" under a given directory.

    Note:
        A collection is defined as a flat folder (IE, no sub-folders) with image contents.
        Any non-image files will be ignored. So long as a folder contains one or more
        images and has no sub-directories, it will be treated as a collection.
    :param root_dir: path to directory to recursively scan through.
    :return: list of Collection objects.
    """
    collection_list = []
    for dir_tuple in (x for x in walk(root_dir)):
        if is_collection(dir_tuple):
            collection_list.append(Collection.from_dir_tuple(dir_tuple))

    return collection_list


def stage_collection_in_database(collection: Collection, session: Session) -> CollectionRecord:
    """
    Stages a given Collection object in the database as a CollectionRecord.
    :param collection: Collection object.
    :param session: database session.
    :return: CollectionRecord generated from input collection.
    """
    collection_record = CollectionRecord.from_collection(collection)
    session.add(collection_record)
    session.flush()
    return collection_record


def stage_images_in_database(images: list, collection_record: CollectionRecord, session: Session):
    """
    Stages all images from the given collection record in a database as ImageRecords.
    :param images: list of Image objects.
    :param collection_record: CollectionRecord object corresponding to the image set.
    :param session: database session.
    """
    for image in images:
        image_record = ImageRecord.from_image(image, collection_record)
        session.add(image_record)


def make_sure_path_exists(path):
    try:
        Path(path).mkdir()
    except OSError as exception:
        if exception.errno != EEXIST:
            raise


@click.command()
@click.argument("target_dir", type=click.Path(exists=True))
def main(target_dir: Path):
    logging.info("Initializing database.")
    initialize_database()
    logging.info(f"Collecting photos and sub-directories of \"{target_dir}\".")
    collections = scan(str(target_dir))

    session = get_session()

    for collection in collections:
        collection_record = stage_collection_in_database(collection, session)
        stage_images_in_database(collection.images, collection_record, session)
        logging.info(f"{collection.name} : {len(collection.images)} : {collection.path}")

    logging.info("Adding new items to database.")
    session.flush()
    session.commit()
    logging.info("Complete.")


if __name__ == "__main__":
    log_dir = "logs"
    log_file = f"database-builder {datetime.now()}.log"
    make_sure_path_exists(log_dir)

    file_handler = logging.FileHandler(f"{log_dir}/{log_file}")
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logging.basicConfig(handlers=[file_handler, stream_handler],
                        level=logging.DEBUG,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
