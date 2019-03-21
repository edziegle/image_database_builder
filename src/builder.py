#!/usr/bin/env python3

from pathlib import Path

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

from logger import get_logger


def get_sub_items(path):
    return [x for x in path.glob('*') if x.is_dir() or is_image(x)]


def is_image(path):
    path_name = path.name
    for extension in ('.jpeg', '.jpg', '.png', '.gif'):
        if extension in path_name:
            return True
    return False


@click.command()
@click.argument('target_dir', type=click.Path(exists=True))
def main(target_dir):
    logger = get_logger()
    parent_path = Path(target_dir)
    logger.info(f'Collecting photos and subdirectories of \'{parent_path}\'.')
    if parent_path.is_dir():
        sub_items = get_sub_items(parent_path)
        logger.info(sub_items)
    else:
        logger.critical(f'Not a directory: {parent_path}')


if __name__ == '__main__':
    main()
