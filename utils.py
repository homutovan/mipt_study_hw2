import os
import sys
from logging import DEBUG, NullHandler, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler

from settings import VERBOSE, log_file, log_path


def get_logger(name):
    """
    """
    if log_file:
        if not os.path.isdir(log_path):
            os.mkdir(log_path)

    stream_handler = StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        f'{log_path}/{name}.log',
        maxBytes=100000,
        backupCount=100,
        ) or NullHandler()
    handlers = []

    if VERBOSE:
        handlers.append(stream_handler)

    if log_file:
        handlers.append(file_handler)

    basicConfig(
        handlers=handlers,
        format='%(asctime)s %(levelname)-5s: %(processName) -25s: %(message)s',
        level=DEBUG,
    )

    logger = getLogger(name)
    logger.disabled = not (VERBOSE or log_file)

    return logger
