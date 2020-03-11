import logging
import sys


def log_module():
    logger = logging.getLogger(__name__)
    if not getattr(logger, 'handler_set', None):
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.handler_set = True
    return logger


def log_inconsistent(component_list, metadata_component):
    if not component_list:
        pass
    else:
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
    if not component_list:
        pass
    else:
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
