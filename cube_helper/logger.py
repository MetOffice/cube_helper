# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import logging
import sys


def log_module():
    logger = logging.getLogger(__name__)
    if not getattr(logger, 'handler_set', None):
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.handler_set = True
    return logger


def log_inconsistent(component_list, metadata_component):
    if component_list:
        logger = log_module()
        msg = ""
        for comp in component_list:
            if len(component_list) == 1:
                msg = "{} ".format(comp)
            elif comp != component_list[-1]:
                msg = msg + "{}, ".format(comp)
            else:
                msg = msg + "and {} ".format(comp)
        msg = "\t" + msg + metadata_component + " inconsistent\n"
        logger.info(msg)


def log_coord_remove(component_list, metadata_component):
    if component_list:
        logger = log_module()
        msg = ""
        for comp in component_list:
            if len(component_list) == 1:
                msg = "{} ".format(comp)
            elif comp != component_list[-1]:
                msg = msg + "{}, ".format(comp)
            else:
                msg = msg + "and {} ".format(comp)
        msg = "Deleting " + msg + metadata_component + " from cubes\n"
        logger.info(msg)
