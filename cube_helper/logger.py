# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import logging
import sys


class CapturableHandler(logging.StreamHandler):

    @property
    def stream(self):
        return sys.stdout

    @stream.setter
    def stream(self, value):
        pass


def _add_handler(logger, level, handler):
    logger.setLevel(level)
    handler = handler
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.handler_set = True


def _remove_handler(logger):
    logger.handlers.pop()
    logger.handler_set = False


def log_module():
    logger = logging.getLogger(__name__)
    handler = CapturableHandler()
    if not getattr(logger, 'handler_set', None):
        _add_handler(logger, logging.INFO, handler)
    return logger


def muffle_logger():
    """
    A function that switches the logging level to ``ERROR`` or higher, thereby
    muffling all output other than error messages. As this
    option obscures the user to changes made to cubes on load
    (as well as inconsistencies) it is advised not to use this
    function unless absolutely necessary.
    """
    logger = logging.getLogger(__name__)
    handler = CapturableHandler()
    if getattr(logger, 'handler_set', None):
        _remove_handler(logger)
        _add_handler(logger, logging.ERROR, handler)
    else:
        _add_handler(logger, logging.ERROR, handler)


def reset_logger():
    """
    A function that switches the level to ``INFO`` or higher, allowing
    ``cube_helper``'s logger to detail changes and inconsistencies as
    usual
    """
    logger = logging.getLogger(__name__)
    handler = CapturableHandler()
    if getattr(logger, 'handler_set', None):
        _remove_handler(logger)
        _add_handler(logger, logging.INFO, handler)
    else:
        _add_handler(logger, logging.INFO, handler)


def _to_comma_and_str(component_list, metadata_component):
    if len(component_list) > 1:
        msg = ", ".join(component_list[:-1]) + " and " + component_list[-1]
        return msg + ' ' + metadata_component
    elif len(component_list) == 1:
        msg = component_list[0]
        return msg + ' ' + metadata_component
    else:
        msg = ""
        return str(msg + metadata_component)


def log_inconsistent(component_list, metadata_component):
    logger = log_module()
    if component_list:
        msg = "\t" + \
              _to_comma_and_str(component_list, metadata_component) + \
              " inconsistent\n"
        logger.info(str(msg))


def log_coord_remove(component_list, metadata_component):
    logger = log_module()
    if component_list:
        msg = ""
        for comp in component_list:
            if len(component_list) == 1:
                msg = "{} ".format(comp)
            elif comp != component_list[-1]:
                msg = msg + "{}, ".format(comp)
            else:
                msg = msg + "and {} ".format(comp)
        msg = "Deleting " + \
              _to_comma_and_str(component_list, metadata_component) + \
              " from cubes\n"
        logger.info(str(msg))
