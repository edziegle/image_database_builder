import errno
import logging
from pathlib import Path


def make_sure_path_exists(path):
    try:
        Path(path).mkdir()
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_logger():
    """Returns a configured logger"""
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
