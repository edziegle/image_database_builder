#!/usr/bin/env python3
from os import walk
from pathlib import Path
from sqlalchemy import create_engine

# photos stuff
# collect parent directory from user
# gather all folders and sub folders
# -- each folder becomes an album(choose name?)
# gather all photos, grouped by folder

# database stuff
# create new database
# -- what if it already exists?
# create collections table
# create photos table
# create records
import click

from collection import Collection, is_collection
from logger import get_logger

engine = create_engine('sqlite:///image_database.db')


def scan(root_dir: str) -> list:
    collection_list = []
    for dir_tuple in (x for x in walk(root_dir)):
        if is_collection(dir_tuple):
            collection_list.append(Collection.from_dir_tuple(dir_tuple))

    return collection_list


@click.command()
@click.argument('target_dir', type=click.Path(exists=True))
def main(target_dir: Path):
    logger = get_logger()
    logger.info(f'Collecting photos and subdirectories of \'{target_dir}\'.')
    collections = scan(str(target_dir))
    logger.info(collections)


if __name__ == '__main__':
    main()
