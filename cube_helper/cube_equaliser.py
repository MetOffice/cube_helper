# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

from __future__ import (absolute_import, division, print_function)
import numpy as np
from collections import namedtuple
from itertools import combinations
from cube_helper.logger import log_module, log_inconsistent, log_coord_remove

from iris.util import unify_time_units


def equalise_attributes(cubes, comp_only=False):
    """
    Equalises Cubes for concatenation and merging, cycles through the
    iterable of cubes (either a list of loaded cubes or aan iris CubeList)
    and removes any that are not common across all cubes, metadata,
    and variables.

    Args:
        cubes: Cubes to be equalised of attributes.

        comp_only: A boolean value, if set to True it will examine
        the cubes attributes and print inconsistencies
        but not equalise them.

    Returns:
        Equalised cube_dataset to the CubeHelp class

    """
    uncommon_keys = set()
    attr_dict_list = []
    attr_dict = {}
    for cube in cubes:
        for key, value in cube.attributes.items():
            if isinstance(value, np.ndarray):
                value = str(value)
                attr_dict.update({key: value})
            else:
                attr_dict.update({key: value})
        attr_dict_list.append(attr_dict.items())
        attr_dict = {}
    combs = list(combinations(attr_dict_list, 2))
    for element in combs:
        for key in set(element[0]) ^ set(element[1]):
            uncommon_keys.add(key[0])

    if not comp_only:
        for key in uncommon_keys:
            for cube in cubes:
                try:
                    del cube.attributes[key]
                except KeyError:
                    pass
        log_coord_remove(list(uncommon_keys), 'attributes')
    else:
        log_inconsistent(list(uncommon_keys), 'attributes')
    return cubes


def equalise_time_units(cubes, comp_only=False):
    """
    Equalises time units by cycling through each cube in the given CubeList
    or list of loaded cubes.

    Args:
        cubes: Cubes to equalised of time coords.

        comp_only: A boolean value, if set to True it will examine
        the cubes time_coordinates and print inconsistencies but not
        equalise them.

    Returns:
        cubes with time coordinates unified.
    """
    logger = log_module()
    comp_messages = set()
    change_messages = set()
    calendar = cubes[0].coord('time').units.calendar
    origin = cubes[0].coord('time').units.origin
    for cube in cubes:
        for time_coord in cube.coords():
            if time_coord.units.is_time_reference():
                if comp_only:
                    if time_coord.units.calendar != calendar:
                        comp_messages.add("\tcalendar format inconsistent\n")
                    if time_coord.units.origin != origin:
                        comp_messages.add("\ttime start date inconsistent\n")
                else:
                    if origin != time_coord.units.origin:
                        change_messages.add("New time origin set to "
                                            "{}\n".format(origin))
                        unify_time_units(cubes)
    if comp_messages:
        for message in comp_messages:
            logger.info(message)
    if change_messages:
        for message in change_messages:
            logger.info(message)

    return cubes


def equalise_data_type(cubes, data_type='float32'):
    """
    Casts datatypes in iris numpy array to be of the same datatype.

    Args:
        cubes: Cubes to have their datatypes equalised.

        data_type: String specifying datatype, default is float32.


    Returns:
        cubes: Cubes with their data types identical.
    """
    logger = log_module()
    if data_type == 'float32':
        for cube in cubes:
            cube.data = np.float32(cube.data)
    elif data_type == 'float64':
        for cube in cubes:
            cube.data = np.float64(cube.data)
    elif data_type == 'int32':
        for cube in cubes:
            cube.data = np.int32(cube.data)
    elif data_type == 'int64':
        for cube in cubes:
            cube.data = np.int64(cube.data)
    else:
        logger.error("invalid data type")


def equalise_dim_coords(cubes, comp_only=False):
    """
    Equalises dimensional coordinates of Cubes, specifically long_name,
    standard_name, and var_name.

    Args:
        cubes: CubeList or list of Cubes to equalise.

        comp_only: A boolean value, if set to True it will examine
        the cubes dimension coordinates and print inconsistencies
        but not equalise them.

    Returns:
        Cubes equalised across dimension coordinates.
    """
    logger = log_module()
    inconsistency_sn = set()
    inconsistency_ln = set()
    inconsistency_vn = set()
    inconsistency_attr = set()
    coord_dict = {}
    for cube in cubes:
        for coord in cube.dim_coords:
            coord_dict.update(
                {coord.name(): {'long_name': coord.long_name,
                                'standard_name': coord.standard_name,
                                'var_name': coord.var_name,
                                'attributes': coord.attributes}})

    for coord in coord_dict:
        for cube in cubes:
            if comp_only:
                if cube.coord(coord).standard_name != \
                        coord_dict[coord]['standard_name']:
                    inconsistency_sn.add(coord)
                if cube.coord(coord).long_name != \
                        coord_dict[coord]['long_name']:
                    inconsistency_ln.add(coord)
                if cube.coord(coord).var_name != \
                        coord_dict[coord]['var_name']:
                    inconsistency_vn.add(coord)
                if cube.coord(coord).attributes != \
                        coord_dict[coord]['attributes']:
                    inconsistency_attr.add(coord)
            else:
                try:
                    cube.coord(coord).standard_name = \
                        coord_dict[coord]['standard_name']
                    cube.coord(coord).long_name = \
                        coord_dict[coord]['long_name']
                    cube.coord(coord).var_name = \
                        coord_dict[coord]['var_name']
                    cube.coord(coord).attributes = \
                        coord_dict[coord]['attributes']
                except ValueError:
                    pass
    if any([inconsistency_sn,
            inconsistency_ln,
            inconsistency_vn,
            inconsistency_attr]):
        logger.info("\ncube dim coordinates differ: \n")
    if comp_only:
        log_inconsistent(list(inconsistency_sn), 'coords standard_name')
        log_inconsistent(list(inconsistency_ln), 'coords long_name')
        log_inconsistent(list(inconsistency_vn), 'coords var_name')
        log_inconsistent(list(inconsistency_attr), 'coords attributes')
    return cubes


def equalise_aux_coords(cubes, comp_only=False):
    """
    Equalises auxiliary coordinates of cubes.

    Args:
        cubes: CubeList or list of Cubes to equalise.

        comp_only: A boolean value, if set to True it will examine
        the Cube's aux coordinates and print inconsistencies
        but not equalise them.

    Returns:
        Cubes equalised across auxiliary coordinates.
    """
    logger = log_module()
    inconsistencies = set({})
    change_messages = set({})
    cube_combs = list(combinations(cubes, 2))
    for combs in cube_combs:
        cube_a_dict = {c.name(): c for c in combs[0].aux_coords}
        cube_b_dict = {c.name(): c for c in combs[1].aux_coords}
        cube_a_coords = {c for c in cube_a_dict}
        cube_b_coords = {c for c in cube_b_dict}
        for coord in list(cube_a_coords):
            if coord not in cube_b_coords:
                if comp_only:
                    inconsistencies.add(coord)
                elif coord == 'height':
                    change_messages.add("Adding {} coords to cube\n".
                                        format(coord))
                    combs[1].add_aux_coord(cube_a_dict[coord])
        for coord in list(cube_b_coords):
            if coord not in cube_a_coords:
                if comp_only:
                    inconsistencies.add(coord)
                elif coord == 'height':
                    change_messages.add("Adding {} coords to cube\n".
                                        format(coord))
                    combs[0].add_aux_coord(cube_b_dict[coord])
    if inconsistencies:
        inconsistencies = list(inconsistencies)
        log_inconsistent(inconsistencies, 'coords')

    if change_messages:
        for message in change_messages:
            logger.info(message)

    return cubes


def remove_attributes(cubes):
    """
    Sets all cube attributes to an empty string.
    be unaffected.

    Args:
        cubes: Cubes to have attributes stripped.

    Returns:
        Cubes with attributes replaced with empty string ''.
    """
    for cube in cubes:
        for attr in cube.attributes:
            cube.attributes[attr] = ''


def equalise_all(cubes):
    """
    Invokes equalise_aux_coords, equalise_attributes,
    equalise_dim_coords and equalise_time units all at once.
    Used before cube_load concatenates the cubes.

    Args:
        cubes: Cubes to be equalised.

    Returns:
        cubes: Cubes equalised across metadata and coords.


    """
    cubes = equalise_aux_coords(cubes)
    cubes = equalise_attributes(cubes)
    cubes = equalise_dim_coords(cubes)
    cubes = equalise_time_units(cubes)
    return cubes


def compare_cubes(cubes):
    """
    Examines coordinates and attributes across iterable of iris cubes
    And calls equalise functions (with comp_only arg set to true) where
    appropriate.

    Args:
        cubes: An iterable of iris Cubes or CubeList to be compared
        for inconsistencies.

    Returns:
        A printed string detailing the inconsistencies in the cubes.
    """
    logger = log_module()
    uneq_aux_coords = False
    uneq_dim_coords = False
    uneq_attr = False
    uneq_time_coords = False
    uneq_ndim = False
    cube_combs = list(combinations(cubes, 2))
    for comb in cube_combs:
        if (uneq_aux_coords and
                uneq_attr and
                uneq_dim_coords and
                uneq_time_coords and
                uneq_ndim):
            break

        if comb[0].aux_coords != comb[1].aux_coords:
            uneq_aux_coords = True

        if comb[0].dim_coords != comb[1].dim_coords:
            uneq_dim_coords = True

        if comb[0].attributes != comb[1].attributes:
            uneq_attr = True

        if comb[0].ndim != comb[1].ndim:
            uneq_ndim = True
            break

        if comb[0].coord('time').units != comb[1].coord('time').units:
            uneq_time_coords = True
            break

    if uneq_ndim:
        logger.error("Number of dimensions for cubes differ,"
                     " please load cubes of matching ndim")
        raise OSError

    if uneq_aux_coords:
        logger.info("\ncube aux coordinates differ: \n")
        equalise_aux_coords(cubes, comp_only=True)

    if uneq_dim_coords:
        equalise_dim_coords(cubes, comp_only=True)

    if uneq_attr:
        logger.info("cube attributes differ: \n")
        equalise_attributes(cubes, comp_only=True)

    if uneq_time_coords:
        logger.info("cube time coordinates differ: \n")
        equalise_time_units(cubes, comp_only=True)


def _examine_dim_bounds(cubes, cube_files):
    Range = namedtuple('Range', ['start', 'end'])
    msg = ''
    for i, cube_a in enumerate(cubes):
        for j, cube_b in enumerate(cubes):
            if i != j:
                range_a = Range(start=cube_a.coord('time').bounds[0][0],
                                end=cube_a.coord('time').bounds[-1][-1])
                range_b = Range(start=cube_b.coord('time').bounds[0][0],
                                end=cube_b.coord('time').bounds[-1][-1])
                latest_start = max(range_a.start, range_b.start)
                earliest_end = min(range_a.end, range_b.end)
                delta = earliest_end - latest_start
                overlap = max(0, delta)
                if overlap > 0:
                    msg = msg + "\nThe time coordinates overlap at cube {}" \
                                " and cube {}".format(i, j)
                    msg = msg + "\nThese cubes are: \n\t{}\n\t{}"\
                        .format(cube_files[i], cube_files[j])
                    break
    return msg


def examine_dim_bounds(cubes, cube_files):
    """
    Examines the dimensional bounds of time should concatenate fail.
    Cycles through cubes and determines if the times are contiguous.

    Args:
         cubes: Iris cubes to examine the time bounds of

         cube_files: the respective files of cubes, to give users
         info as to what cubes are causing problems with concatenation.

    Returns:
        A printed string detailing any overlap in the time bounds.
    """
    logger = log_module()
    msg = _examine_dim_bounds(cubes, cube_files)
    logger.info(msg)
