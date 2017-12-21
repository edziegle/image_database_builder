#!/usr/bin/env python3

import argparse
import logging
import errno
from pathlib import Path


# photos stuff
# collect parent directory from user
# gather all folders and sub folders
# -- each folder becomes an album(choose name?)
# gather all photos, grouped by folder

# database stuff
# create new database
# -- what if it already exists?
# create photos table
# create records


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='Parent directory to scan and create database from.')
    return parser.parse_args()


# todo rename me
def make_sure_path_exists(path):
    try:
        Path(path).mkdir()
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_logger():
    new_logger = logging.getLogger('database_builder')
    new_logger.setLevel(logging.DEBUG)
    make_sure_path_exists('logs')

    file_handler = logging.FileHandler('logs/database_builder.log')
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    new_logger.addHandler(file_handler)
    new_logger.addHandler(stream_handler)
    return new_logger


if __name__ == '__main__':
    args = parse_args()
    logger = get_logger()

    parent_path = Path(args.directory)
    logger.info('Collecting photos and subdirectories of \'{}\'.'.format(parent_path))
    if parent_path.is_dir():
        logger.info('cool')
    else:
        logger.critical('Not a directory: {}'.format(parent_path.name))
