import logging
import sys


def log_module():
    logger = logging.getLogger('cube_helper')
    if not getattr(logger, 'handler_set', None):
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('cube_helper:\t%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.handler_set = True
    return logger

