#!/usr/bin/env python3
import logging
from errno import EEXIST
from os import walk
from pathlib import Path
from datetime import datetime

import click

from collection import Collection, is_collection
from database import initialize_database, get_session, CollectionRecord, ImageRecord


def scan(root_dir: str) -> list:
    collection_list = []
    for dir_tuple in (x for x in walk(root_dir)):
        if is_collection(dir_tuple):
            collection_list.append(Collection.from_dir_tuple(dir_tuple))

    return collection_list


@click.command()
@click.argument('target_dir', type=click.Path(exists=True))
def main(target_dir: Path):
    logging.info("Initializing database.")
    initialize_database()
    logging.info(f'Collecting photos and subdirectories of \'{target_dir}\'.')
    collections = scan(str(target_dir))

    session = get_session()

    for collection in collections:
        collection_record = stage_collections_in_database(collection, session)
        stage_images_in_database(collection, collection_record, session)
        logging.info(f"{collection.name} : {len(collection.images)} : {collection.path}")

    logging.info("Adding new items to database.")
    session.flush()
    session.commit()
    logging.info("Complete.")


def stage_images_in_database(collection, collection_record, session):
    for image in collection.images:
        image_record = ImageRecord.from_image(image, collection_record)
        session.add(image_record)


def stage_collections_in_database(collection, session):
    collection_record = CollectionRecord.from_collection(collection)
    session.add(collection_record)
    session.flush()
    return collection_record


def make_sure_path_exists(path):
    try:
        Path(path).mkdir()
    except OSError as exception:
        if exception.errno != EEXIST:
            raise


if __name__ == '__main__':
    log_dir = 'logs'
    log_file = f'database-builder {datetime.now()}.log'
    make_sure_path_exists(log_dir)

    file_handler = logging.FileHandler(f'{log_dir}/{log_file}')
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logging.basicConfig(handlers=[file_handler, stream_handler],
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
